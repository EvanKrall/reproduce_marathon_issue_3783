from behave import when, given, then
import marathon
import time


def wait_for_marathon(context):
    for _ in xrange(30):
        try:
            context.client.ping()
        except marathon.exceptions.MarathonError:
            time.sleep(1)
        else:
            return


def delete_existing_apps(context):
    for app in context.client.list_apps():
        context.client.delete_app(app.id, force=True)
    # app deletes seem to be asynchronous, creating an app with the same name
    # as a previous app will fail unless the deploy for deleting it has
    # finished.
    time.sleep(0.5)
    while context.client.list_deployments():
        print "There are still marathon deployments in progress. sleeping."
        time.sleep(0.5)


@given('a running marathon instance')
def running_marathon_instance(context):
    context.client = marathon.MarathonClient('http://marathon:8080/')
    wait_for_marathon(context)
    delete_existing_apps(context)


@given('a marathon app for marathon to start')
def marathon_app_for_marathon_to_start(context):
    context.client.create_app(
        app_id='app-id',
        app=marathon.MarathonApp(
            cmd="/bin/sleep 300",
            container={
                'docker': {
                    'image': 'busybox',
                    'network': 'BRIDGE',
                },
                'type': 'DOCKER',
            },
            # This constraint  will prevent more than one instance from
            # starting, ensuring the marathon deploy is still running when we
            # cause a failover.
            constraints=[["hostname", "UNIQUE"]],
            instances=2,
            health_checks=[
                marathon.models.MarathonHealthCheck(
                    protocol="COMMAND",
                    command={"value": "/bin/true"},
                    gracePeriodSeconds=300,
                )
            ]
        ),
    )


@when('we wait for one of the instances to start')
def wait_for_one_instance_to_start(context):
    for _ in xrange(60):
        app = context.client.get_app('app-id', embed_tasks=True)
        if app.tasks_running >= 1:
            context.task_ids_before_failover = set([t.id for t in app.tasks])
            return
        time.sleep(1)

    raise Exception("Instance did not start before timeout. Tasks: %r" % app.tasks)


@when('we cause a leadership failover')
def cause_a_leadership_failover(context):
    context.client.delete_leader()


@then('marathon should not kill anything')
def marathon_should_not_kill_anything(context):
    app = context.client.get_app('app-id', embed_tasks=True)
    # Check for a little while, in case the effect is delayed.
    for _ in xrange(10):
        task_ids = set([t.id for t in app.tasks])
        assert context.task_ids_before_failover == task_ids
        time.sleep(1)
