require 'spec_helper'

describe "evidences/index.html.erb" do
  before(:each) do
    assign(:evidences, [
      stub_model(Evidence,
        :hunch_id => 1,
        :title => "Title",
        :description => "MyText",
        :rating => 1
      ),
      stub_model(Evidence,
        :hunch_id => 1,
        :title => "Title",
        :description => "MyText",
        :rating => 1
      )
    ])
  end

  it "renders a list of evidences" do
    render
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => 1.to_s, :count => 2
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => "Title".to_s, :count => 2
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => "MyText".to_s, :count => 2
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    assert_select "tr>td", :text => 1.to_s, :count => 2
  end
end
