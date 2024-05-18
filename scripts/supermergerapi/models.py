from pydantic import BaseModel, Field


#class SingleImageRequest(BaseModel):
#    image: str = Field(default="", title="Image", description="Image to work on, must be a Base64 string containing the image's data.")
#
class SingleImageResponse(BaseModel):
    image: str = Field(default="", title="Image", description="Generated image, a Base64 string containing the image's data.")

class MergeRequest(BaseModel):
    #weights_a: str = Field(default="0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5", title="Weights A", description="")
    #weights_b: str = Field(default="0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5", title="Weights B", description="")
    model_a: str = Field(default="", title="Model A", description="Model A to perform calcs with. I.e. Name of an SD model including extension.")
    model_b: str = Field(default="", title="Model B", description="Model B to perform calcs with. I.e. Name of an SD model including extension.")
    model_c: str = Field(default="", title="Model C", description="Model C to perform calcs with. I.e. Name of an SD model including extension.")
    merge_mode: str = Field(default="Weight sum", title="Merge Mode", description="The model to use when merging. (See get_merge_modes)")
    calculation_mode: str = Field(default="normal", title="Calculation Mode", description="The calculation to use when merging. (See get_calculation_modes)")
    alpha: float = Field(default=0.5, title="Alpha", description="Amount to use in calculation.")
    beta: float = Field(default=0.25, title="Beta", description="Amount to be used in calculation. Not always used as it depends on the calculation mode.")
    #generate_image: = bool Field(default=false,

class MergeResponse(BaseModel):
    result: str = Field(default="", title="Result", description="Operation result.")
    model_name: str = Field(default="", title="Merged Model Name", description="The name of the merged model in memory.")

# Includes everthing from merge request plus plot details
class XYPlotRequest(MergeRequest):
    x_type: str = Field(default="", title="X Type", description="Type of data to use for the X axis (across). (Get types using \get_plot_types)")
    x_type_number: int = Field(default=0, title="", description="Number of items to expect.")
    y_type: str = Field(default="", title="", description="Type of data to use for the Y axis (down).")
    z_type: str = Field(default="", title="", description="")
    # include image generation settings

class SaveModelRequest(BaseModel):
    currentmodel: str | None = Field(default=None, title="Current Model", description="")
    fname: str = Field(default="", title="Filename", description="")
    savesets: list = Field(default=['safetensors'], title="Type", description="")
