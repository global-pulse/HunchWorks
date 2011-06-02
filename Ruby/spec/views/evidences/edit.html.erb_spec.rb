require 'spec_helper'

describe "evidences/edit.html.erb" do
  before(:each) do
    @evidence = assign(:evidence, stub_model(Evidence,
      :hunch_id => 1,
      :title => "MyString",
      :description => "MyText",
      :rating => 1
    ))
  end

  it "renders the edit evidence form" do
    render

    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "form", :action => evidences_path(@evidence), :method => "post" do
      assert_select "input#evidence_hunch_id", :name => "evidence[hunch_id]"
      assert_select "input#evidence_title", :name => "evidence[title]"
      assert_select "textarea#evidence_description", :name => "evidence[description]"
      assert_select "input#evidence_rating", :name => "evidence[rating]"
    end
  end
end
