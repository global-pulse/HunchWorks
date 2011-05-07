Feature: Evidences
  In order to determine whether a hunch is supported
  people need to be able to add evidence to them
  
  Background: Make sure that we have a hunch
    Given I go to the hunches page
    And I follow "New Hunch"
    And I fill in "Title" with "Drought in Sudan"
    And I fill in "Description" with "Hungry season is lasting longer than usual."
    And I press "Create"
    
  Scenario: viewing evidence already added
    When I go to the hunches page
    Then I should see "0 evidences"
    
  Scenario: adding evidence to a hunch
    When I go to the hunches page
    And I follow "+1"
    Then I should see "1 positive"