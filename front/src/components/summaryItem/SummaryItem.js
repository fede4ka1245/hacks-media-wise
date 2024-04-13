import React, {useCallback, useEffect, useMemo, useState} from 'react';
import {Grid, Typography} from "@mui/material";
import {useNavigate} from "react-router-dom";
import {routes} from "../../routes";
import {getStatus} from "../../api";

const status = {
  created: {
    color: 'var(--primary-color)',
    name: 'Загружаю файлик'
  },
  died: {
    color: 'var(--error-color)',
    name: 'Что то пошло не так:('
  },
  loading: {
    color: 'red',
    name: 'loading'
  }
}
const SummaryItem = ({ id }) => {
  const navigate = useNavigate();
  const [state, setState] = useState('loading');

  const onClick = useCallback(() => {
    navigate(routes.model + '/' + id);
  }, [id]);

  useEffect(() => {
    let idInterval;
    const load = async () => {
      await getStatus(id)
        .then((state) => {
          if (state?.detail) {
            return;
          }

          setState(state);
        })

      idInterval = setTimeout(load, 6000);
    }

    load();

    return () => {
      clearTimeout(idInterval);
    }
  }, []);

  const {
    color,
    name
  } = useMemo(() => {
    return status[state] || {
      color: '',
      name: 'loading'
    };
  }, [state]);

  return (
    <Grid
      display={'flex'}
      flexDirection={'column'}
      style={{ backgroundColor: 'var(--bg-color)', cursor: 'pointer' }}
      border={'var(--element-border)'}
      borderRadius={'var(--border-radius-md)'}
      p={'var(--space-sm)'}
      onClick={onClick}
    >
      <Typography
        fontWeight={'1000'}
        fontSize={'22px'}
        userSelect={'none'}
        fontFamily={'Nunito'}
        color={'white'}
      >
         #{id}
      </Typography>
      <Typography
        fontWeight={'600'}
        fontSize={'15px'}
        userSelect={'none'}
        fontFamily={'Nunito'}
        color={'var(--text-secondary-color)'}
      >
        Статус: {name !== 'loading' && <strong style={{ color }}>{name}</strong>}
      </Typography>
    </Grid>
  );
};

export default SummaryItem;