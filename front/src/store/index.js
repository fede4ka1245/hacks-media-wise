import {configureStore, createAsyncThunk} from '@reduxjs/toolkit';
import React from 'react';
import { createSlice } from '@reduxjs/toolkit';
import { uploadFile as uploadFileApi, getModel as getModelApi } from "../api";
import {pullState} from "../logic";
import camelcaseKeys from 'camelcase-keys';

const getModel = async (id) => {
  await pullState(id, 'ready');

  return await getModelApi(id);
}

const model = {
  isLoading: false,
}

const initialState = {
  loading: false,
  file: null,
  model
};

const uploadFile = createAsyncThunk(
  'main/uploadFile',
  async (file) => {
    return await uploadFileApi(file)
  }
);

const loadModel = createAsyncThunk(
  'main/loadModel',
  async (id) => {
    return await getModel(id)
  }
);


export const mainSlice = createSlice({
  name: 'main',
  initialState,
  reducers: {
  },
  extraReducers: (builder) => {
    builder.addCase(uploadFile.pending, (state) => {
      state.loading = true;
    });
    builder.addCase(loadModel.pending, (state) => {
      state.model.isLoading = true;
    });

    builder.addCase(uploadFile.fulfilled, (state) => {
      state.loading = false;
    });
    builder.addCase(loadModel.fulfilled, (state, action) => {
      state.model = {
        ...state.model,
        isLoading: false,
        ...camelcaseKeys(action.payload, { deep: true }),
      }
    });
  }
})

// const {
//   setDate,
//   setEvent
// } = mainSlice.actions;

export {
  uploadFile,
  loadModel
};

export default configureStore({
  reducer: {
    main: mainSlice.reducer,
  }
});