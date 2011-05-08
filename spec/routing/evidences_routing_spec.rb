require "spec_helper"

describe EvidencesController do
  describe "routing" do

    it "recognizes and generates #index" do
      { :get => "/evidences" }.should route_to(:controller => "evidences", :action => "index")
    end

    it "recognizes and generates #new" do
      { :get => "/evidences/new" }.should route_to(:controller => "evidences", :action => "new")
    end

    it "recognizes and generates #show" do
      { :get => "/evidences/1" }.should route_to(:controller => "evidences", :action => "show", :id => "1")
    end

    it "recognizes and generates #edit" do
      { :get => "/evidences/1/edit" }.should route_to(:controller => "evidences", :action => "edit", :id => "1")
    end

    it "recognizes and generates #create" do
      { :post => "/evidences" }.should route_to(:controller => "evidences", :action => "create")
    end

    it "recognizes and generates #update" do
      { :put => "/evidences/1" }.should route_to(:controller => "evidences", :action => "update", :id => "1")
    end

    it "recognizes and generates #destroy" do
      { :delete => "/evidences/1" }.should route_to(:controller => "evidences", :action => "destroy", :id => "1")
    end

  end
end
