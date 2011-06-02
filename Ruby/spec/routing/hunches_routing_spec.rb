require "spec_helper"

describe HunchesController do
  describe "routing" do

    it "recognizes and generates #index" do
      { :get => "/hunches" }.should route_to(:controller => "hunches", :action => "index")
    end

    it "recognizes and generates #new" do
      { :get => "/hunches/new" }.should route_to(:controller => "hunches", :action => "new")
    end

    it "recognizes and generates #show" do
      { :get => "/hunches/1" }.should route_to(:controller => "hunches", :action => "show", :id => "1")
    end

    it "recognizes and generates #edit" do
      { :get => "/hunches/1/edit" }.should route_to(:controller => "hunches", :action => "edit", :id => "1")
    end

    it "recognizes and generates #create" do
      { :post => "/hunches" }.should route_to(:controller => "hunches", :action => "create")
    end

    it "recognizes and generates #update" do
      { :put => "/hunches/1" }.should route_to(:controller => "hunches", :action => "update", :id => "1")
    end

    it "recognizes and generates #destroy" do
      { :delete => "/hunches/1" }.should route_to(:controller => "hunches", :action => "destroy", :id => "1")
    end

  end
end
