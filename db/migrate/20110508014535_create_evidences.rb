class CreateEvidences < ActiveRecord::Migration
  def self.up
    create_table :evidences do |t|
      t.integer :hunch_id
      t.string :title
      t.text :description
      t.integer :rating

      t.timestamps
    end
  end

  def self.down
    drop_table :evidences
  end
end
