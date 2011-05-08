require 'spec_helper'

describe "hunches/new.html.erb" do
  before(:each) do
    assign(:hunch, stub_model(Hunch,
      :title => "MyString",
      :description => "MyText",
      :Geographicarea => "MyText",
      :Sector => "MyText"
    ).as_new_record)
  end

  it "renders new hunch form" do
    render

    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "form", :action => hunches_path, :method => "post" do
      assert_select "input#hunch_title", :name => "hunch[title]"
      assert_select "textarea#hunch_description", :name => "hunch[description]"
      assert_select "textarea#hunch_Geographicarea", :name => "hunch[Geographicarea]"
      assert_select "textarea#hunch_Sector", :name => "hunch[Sector]"
    end
  end
end
