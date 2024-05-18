import os

import gradio as gr
from fastapi import FastAPI, Body, HTTPException, Request, Response
from fastapi.responses import FileResponse

#from .. constants import script_static_dir
#from .. import script as eye_mask_script
#from . utils import encode_pil_to_base64, decode_base64_to_image
import supermerger
from mergers import mergers,model_util
from .models import MergeRequest,MergeResponse,SaveModelRequest
from .constants import API_DEFAULT_WPRESET_SD

class SuperMergerApi():

    def __init__(self):
        pass

    BASE_PATH = '/sdapi/v1/supermerge'
    VERSION = 1
    
    def get_path(self, path):
        return f"{self.BASE_PATH}/v{self.VERSION}{path}"

    def add_api_route(self, path: str, endpoint, **kwargs):
        # authenticated requests can be implemented here
        return self.app.add_api_route(self.get_path(path), endpoint, **kwargs)

    def start(self, _: gr.Blocks, app: FastAPI):
        self.app = app
        # lists
        self.add_api_route('/get_merge_modes', self.get_merge_modes, methods=['GET'])
        self.add_api_route('/get_calculation_modes', self.get_calculation_modes, methods=['GET'])
        #self.add_api_route('/get_xyz_plot_types', self.get_xyz_plot_types, methods=['GET'])
        # ops
        self.add_api_route('/merge', self.merge, methods=['POST'], response_model=MergeResponse)
        self.add_api_route('/savemodel', self.savemodel, methods=['POST'])
        self.add_api_route('/clearcache', self.clearcache, methods=['POST'])
        #self.add_api_route('/xyz_plot', self.xyz_plot, methods=['POST'], response_model=SingleImageResponse)
        ##self.add_api_route('/static/{path:path}', self.static, methods=['GET'])
        ##self.add_api_route('/config.json', self.get_config, methods=['GET'])
    

    def get_merge_modes(self):
        ''' Get merge mode list '''
        return { 'merge_modes': list(mergers.MODES) }
        
    def get_calculation_modes(self):
        ''' Get xyz plot type list '''
        return { 'calculation_modes': list(supermerger.CALCMODES) }
    
    def clearcache(self):
        mergers.clearcache()
        return { 'result': True }

    def savemodel(self, req:SaveModelRequest):
        response = model_util.savemodel(None,req.currentmodel,req.fname,req.savesets,{})
        return { "result": response }
    
    def merge(self, req:MergeRequest):
        weights_a = "0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
        weights_b = "0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5"
        model_a = req.model_a
        model_b = req.model_b
        model_c = req.model_c
        base_alpha = req.alpha
        base_beta = req.beta
        mode = req.merge_mode
        calcmode = req.calculation_mode
        useblocks = False
        custom_name = None
        save_sets = ['safetensors']
        id_sets = []
        wpresets = API_DEFAULT_WPRESET_SD
        deep = ""
        tensor = ""
        bake_in_vae = None
        opt_value = 0.3
        inex = "Off"
        ex_blocks = []
        ex_elems = ""
        esettings = []
        s_prompt = ""
        s_nprompt = ""
        s_steps = 0
        s_sampler = 0
        s_cfg = 0
        s_seed = 0.0
        s_w = 0
        s_h = 0
        s_batch_size = 1
        genoptions = []
        s_hrupscaler = "Latent"
        s_hr2ndsteps = 0
        s_denois_str = 0.7
        s_hr_scale = 2
        lmode = "off"
        lsets = ['alpha']
        llimits_u = "1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1"
        llimits_l = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
        lseed = -1.0
        lserial = 1.0
        lcustom = "U,0,0,0,0,0,0,0,0,0,0,0,0,R,R,R,R,R,R,R,R,R,R,R,R,R"
        lround = 3.0
        currentmodel = ""
        imggen = False
        txt2imgparams = []
        # do some work here
        mergeResult = mergers.smergegen(weights_a,weights_b,model_a,model_b,model_c,base_alpha,base_beta,mode,
                       calcmode,useblocks,custom_name,save_sets,id_sets,wpresets,deep,tensor,bake_in_vae,opt_value,inex,ex_blocks,ex_elems,
                       esettings,
                       s_prompt,s_nprompt,s_steps,s_sampler,s_cfg,s_seed,s_w,s_h,s_batch_size,
                       genoptions,s_hrupscaler,s_hr2ndsteps,s_denois_str,s_hr_scale,
                       lmode,lsets,llimits_u,llimits_l,lseed,lserial,lcustom,lround,
                       currentmodel,imggen,
                       *txt2imgparams)
        #                  
        #                req.useblocks,req.custom_name,req.save_sets,req.id_sets,req.wpresets,req.deep,req.tensor,req.bake_in_vae,req.opt_value,req.inex,req.ex_blocks,req.ex_elems,
        #                req.esettings,
        #                
        #               s_prompt,s_nprompt,s_steps,s_sampler,s_cfg,s_seed,s_w,s_h,s_batch_size,
        #               genoptions,s_hrupscaler,s_hr2ndsteps,s_denois_str,s_hr_scale,
        #               lmode,lsets,llimits_u,llimits_l,lseed,lserial,lcustom,lround,
        #               currentmodel,imggen,
        #               *txt2imgparams)
        #print("result = ",type(mergeResult),mergeResult)
        return MergeResponse(result = mergeResult[0], model_name = mergeResult[1])

    #def xyz_plot(self, req:XYPlotRequest):
    #    # do some work here
    #    return SingleImageResponse(image=encode_pil_to_base64(mask))

    #def get_xyz_plot_types(self):
    #    ''' Get xyz plot type list '''
    #    return { 'xyz_plot_types': list(mergers.TYPESEG) }

#    def static(self, path: str):
#        ''' Serve static files '''
#        static_file = os.path.join(script_static_dir, path)
#        if static_file is not None:
#            return FileResponse(static_file)
#        raise HTTPException(status_code=404, detail='Static file not found')
#    
#    def get_config(self):
#        return FileResponse('config.json')
