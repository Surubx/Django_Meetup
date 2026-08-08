Feature: Event participation

  Scenario: Guest user visits the events page
    Given a guest user is present
    When the user visits the events page
    Then the user is redirected to login

  Scenario: Logged-in user creates a valid event
    Given a logged-in user is present
    When the user creates a valid event
    Then the event is saved successfully

  Scenario: Logged-in user joins an event
    Given a logged-in attendee is present
    When the user joins an existing event
    Then the event shows the user as an attendee

  Scenario: Logged-in user leaves an event
    Given a logged-in attendee who has joined an event is present
    When the user leaves the event
    Then the event no longer shows the user as an attendee
