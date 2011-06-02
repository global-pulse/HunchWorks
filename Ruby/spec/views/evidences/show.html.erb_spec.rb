require 'spec_helper'

describe "evidences/show.html.erb" do
  before(:each) do
    @evidence = assign(:evidence, stub_model(Evidence,
      :hunch_id => 1,
      :title => "Title",
      :description => "MyText",
      :rating => 1
    ))
  end

  it "renders attributes in <p>" do
    render
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/1/)
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/Title/)
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/MyText/)
    # Run the generator again with the --webrat flag if you want to use webrat matchers
    rendered.should match(/1/)
  end
end
