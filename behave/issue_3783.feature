Feature: Marathon
  Scenario: Marathon should not kill tasks on leadership abdication
    Given a running marathon instance
      And a marathon app for marathon to start
     When we wait for one of the instances to start
      And we cause a leadership failover
     Then marathon should not kill anything
     When we cause a leadership failover
     Then marathon should not kill anything
     When we cause a leadership failover
     Then marathon should not kill anything
     When we cause a leadership failover
     Then marathon should not kill anything
     When we cause a leadership failover
     Then marathon should not kill anything
     When we cause a leadership failover
     Then marathon should not kill anything
     When we cause a leadership failover
     Then marathon should not kill anything
