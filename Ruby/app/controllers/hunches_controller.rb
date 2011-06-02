class HunchesController < ApplicationController
  # GET /hunches
  # GET /hunches.xml
  def index
    @hunches = Hunch.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @hunches }
    end
  end

  # GET /hunches/1
  # GET /hunches/1.xml
  def show
    @hunch = Hunch.find(params[:id])
    
    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @hunch }
    end
  end

  # GET /hunches/new
  # GET /hunches/new.xml
  def new
    @hunch = Hunch.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @hunch }
    end
  end

  # GET /hunches/1/edit
  def edit
    @hunch = Hunch.find(params[:id])
  end

  # POST /hunches
  # POST /hunches.xml
  def create
    @hunch = Hunch.new(params[:hunch])

    respond_to do |format|
      if @hunch.save
        format.html { redirect_to(hunches_path, :notice => 'Hunch was successfully created.') }
        format.xml  { render :xml => @hunch, :status => :created, :location => @hunch }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @hunch.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /hunches/1
  # PUT /hunches/1.xml
  def update
    @hunch = Hunch.find(params[:id])

    respond_to do |format|
      if @hunch.update_attributes(params[:hunch])
        format.html { redirect_to(@hunch, :notice => 'Hunch was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @hunch.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /hunches/1
  # DELETE /hunches/1.xml
  def destroy
    @hunch = Hunch.find(params[:id])
    @hunch.destroy

    respond_to do |format|
      format.html { redirect_to(hunches_url) }
      format.xml  { head :ok }
    end
  end
end
