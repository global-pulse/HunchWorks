require 'spec_helper'

describe "hunches/index.html.erb" do
  before(:each) do
    assign(:hunches, [
      stub_model(Hunch,
        :title => "Title",
        :description => "MyText",
        :Geographicarea => "MyText",
        :Sector => "MyText"
      ),
      stub_model(Hunch,
        :title => "Title",
        :description => "MyText",
        :Geographicarea => "MyText",
        :Sector => "MyText"
      )
    ])
  end

  it "renders a list of hunches" do
    render
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => "Title".to_s, :count => 2
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
  end
end
