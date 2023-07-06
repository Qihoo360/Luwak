#!/bin/bash
echo "Merge model parts in ./pretrained_model to full model"
cat ./pretrained_model/model_state.pdparams.part-* > ./pretrained_model/model_state.pdparams
