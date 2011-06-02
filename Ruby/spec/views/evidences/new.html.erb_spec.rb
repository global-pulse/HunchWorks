require 'spec_helper'

describe "evidences/new.html.erb" do
  before(:each) do
    assign(:evidence, stub_model(Evidence,
      :hunch_id => 1,
      :title => "MyString",
      :description => "MyText",
      :rating => 1
    ).as_new_record)
  end

  it "renders new evidence form" do
    render

    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "form", :action => evidences_path, :method => "post" do
      assert_select "input#evidence_hunch_id", :name => "evidence[hunch_id]"
      assert_select "input#evidence_title", :name => "evidence[title]"
      assert_select "textarea#evidence_description", :name => "evidence[description]"
      assert_select "input#evidence_rating", :name => "evidence[rating]"
    end
  end
end
