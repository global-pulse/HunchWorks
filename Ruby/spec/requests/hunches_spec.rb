require 'spec_helper'

describe "Hunches" do
  describe "GET /hunches" do
    it "works! (now write some real specs)" do
      # Run the generator again with the --webrat flag if you want to use webrat methods/matchers
      get hunches_path
      response.status.should be(200)
    end
  end
end
