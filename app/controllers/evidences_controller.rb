class EvidencesController < ApplicationController
  # GET /evidences
  # GET /evidences.xml
  def index
    @evidences = Evidence.all

    respond_to do |format|
      format.html # index.html.erb
      format.xml  { render :xml => @evidences }
    end
  end

  # GET /evidences/1
  # GET /evidences/1.xml
  def show
    @evidence = Evidence.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.xml  { render :xml => @evidence }
    end
  end

  # GET /evidences/new
  # GET /evidences/new.xml
  def new
    @evidence = Evidence.new

    respond_to do |format|
      format.html # new.html.erb
      format.xml  { render :xml => @evidence }
    end
  end

  # GET /evidences/1/edit
  def edit
    @evidence = Evidence.find(params[:id])
  end

  # POST /evidences
  # POST /evidences.xml
  def create
    @evidence = Evidence.new(params[:evidence])

    respond_to do |format|
      if @evidence.save
        format.html { redirect_to(@evidence, :notice => 'Evidence was successfully created.') }
        format.xml  { render :xml => @evidence, :status => :created, :location => @evidence }
      else
        format.html { render :action => "new" }
        format.xml  { render :xml => @evidence.errors, :status => :unprocessable_entity }
      end
    end
  end

  # PUT /evidences/1
  # PUT /evidences/1.xml
  def update
    @evidence = Evidence.find(params[:id])

    respond_to do |format|
      if @evidence.update_attributes(params[:evidence])
        format.html { redirect_to(@evidence, :notice => 'Evidence was successfully updated.') }
        format.xml  { head :ok }
      else
        format.html { render :action => "edit" }
        format.xml  { render :xml => @evidence.errors, :status => :unprocessable_entity }
      end
    end
  end

  # DELETE /evidences/1
  # DELETE /evidences/1.xml
  def destroy
    @evidence = Evidence.find(params[:id])
    @evidence.destroy

    respond_to do |format|
      format.html { redirect_to(evidences_url) }
      format.xml  { head :ok }
    end
  end
end
