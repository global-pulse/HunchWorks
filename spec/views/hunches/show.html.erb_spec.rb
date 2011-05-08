require 'spec_helper'

describe "hunches/show.html.erb" do
  before(:each) do
    @hunch = assign(:hunch, stub_model(Hunch,
      :title => "Title",
      :description => "MyText",
      :Geographicarea => "MyText",
      :Sector => "MyText"
    ))
  end

  it "renders attributes in <p>" do
    render
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/Title/)
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/MyText/)
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/MyText/)
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/MyText/)
  end
end
