import React from 'react';
import {Grid} from "@mui/material";
import styles from './Chart.module.css';

const Chart = ({ src }) => {
  return (
    <Grid width={'100%'}>
      <iframe
        className={styles.main}
        src={src}
      />
    </Grid>
  );
};

export default Chart;