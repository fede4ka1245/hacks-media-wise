import React, {useLayoutEffect, useState} from 'react';
import {Backdrop, CircularProgress, Grid} from "@mui/material";
import styles from './Chart.module.css';
import {useInView} from "react-intersection-observer";

const Chart = ({ src }) => {
  const [entered, setEntered] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { ref, inView } = useInView();

  useLayoutEffect(() => {
    if (inView && !entered) {
      setEntered(true);
      setIsLoading(true)
    }
  }, [inView])

  return (
    <Grid position={'relative'} ref={ref} minHeight={480} maxWidth={'100%'} overflow={'hidden'}>
      <Backdrop
        sx={{ color: '#fff', zIndex: 100, position: 'absolute', width: '100%', height: '100%' }}
        open={isLoading}
        onClick={() => {}}
      >
        <Grid
          width={'90px'}
          height={'90px'}
          display={'flex'}
          flexDirection={'column'}
          justifyContent={'center'}
          alignItems={'center'}
          position={'relative'}
        >
          <CircularProgress
            sx={{
              color: 'var(--primary-color)'
            }}
          />
        </Grid>
      </Backdrop>
      {entered && <iframe
        onLoad={() => setTimeout(() => setIsLoading(false), 2400)}
        className={styles.main}
        src={src}
      />}
    </Grid>
  );
};

export default Chart;