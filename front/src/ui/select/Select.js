import * as React from 'react';
import MuiSelect from '@mui/material/Select';
import { styled } from '@mui/material/styles';

const Select = styled(MuiSelect)(({ theme }) => ({
  '& .MuiSelect-iconOutlined': {
    color: 'white !important'
  },

  color: 'var(--text-secondary-color) !important',
  borderRadius: 'var(--border-radius-sm) !important',
  borderColor: 'var(--text-primary-color) !important',

  '& > .MuiSelectLabel-root': {
    color: 'var(--text-primary-color) !important',
  },

  '& > .MuiSelectBase-root > .Mui-disabled': {
    opacity: 0.5,
    '-webkit-text-fill-color': 'var(--text-secondary-color) !important',
  },

  '& > .Mui-focused > .MuiOutlinedSelect-notchedOutline': {
    borderColor: 'var(--text-primary-color) !important',
  },

  '& .MuiOutlinedInput-notchedOutline': {
    borderColor: 'var(--text-primary-color) !important',
  }
}));

export default Select;