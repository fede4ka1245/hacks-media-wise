import React, {useCallback, useEffect, useLayoutEffect, useMemo, useState} from 'react';
import PreloadContentPlacement from "../../components/preloadContentPlacement/PreloadContentPlacement";
import {FormControl, Grid, InputLabel, MenuItem, Typography} from "@mui/material";
import Tabs from "../../ui/tabs/Tabs";
import Tab from "../../ui/tab/Tab";
import Tappable from "../../ui/tappable/Tappable";
import {ArrowBackIosRounded} from "@mui/icons-material";
import {useNavigate, useParams} from "react-router-dom";
import {routes} from "../../routes";
import {useDispatch, useSelector} from "react-redux";
import {loadModel} from "../../store";
import {throttle} from "lodash";
import styles from './Model.module.css';
import {eventBus, events, getSummariesHistory, setSummariesHistory} from "../../logic";
import Button from "../../ui/button/Button";
import Select from "../../ui/select/Select";
import Chart from "../../components/chart/Chart";
import Input from "../../ui/input/Input";
import axios from "axios";

const tabs = {
}

const dates = [
  '04.09.2023',
  '11.09.2023',
  '18.09.2023',
  '25.09.2023',
  '02.10.2023',
  '09.10.2023',
  '16.10.2023',
  '23.10.2023',
  '30.10.2023',
  '06.11.2023',
  '13.11.2023',
  '20.11.2023',
  '27.11.2023',
  '04.12.2023',
  '11.12.2023',
  '18.12.2023',
  '25.12.2023',
  '01.01.2024',
  '08.01.2024',
  '15.01.2024',
  '22.01.2024',
  '29.01.2024',
  '05.02.2024',
  '12.02.2024',
  '19.02.2024',
  '26.02.2024',
  '04.03.2024',
  '11.03.2024',
  '18.03.2024'
];

const API_URL = process.env.REACT_APP_SERVER_API || ''

const features = [
  '10_Медиа ТВ (Моделироуемый бренд)_(1)ТВ, trp(Ж 30-60 ВС)',
  '10_Медиа ТВ (Моделироуемый бренд)_(1)ТВ, рубли',
  '10_Медиа ТВ (Моделироуемый бренд)_(1)ТВ, охват 5+(Ж 30-60 ВС)',
  '10_Медиа ТВ (Моделироуемый бренд)_(тотал)ТВ, trp(Ж 30-60 ВС)',
  '10_Медиа ТВ (Моделироуемый бренд)_(тотал)ТВ, рубли',
  '10_Медиа ТВ (Моделироуемый бренд)_(тотал)ТВ, охват 5+(Ж 30-60 ВС)',
  '11_Медиа Диджитал (Моделируемый бренд)_Диджитал, рубли'
];

function elementInViewport(el) {
  var top = el.offsetTop;
  var height = el.offsetHeight;

  while(el.offsetParent) {
    el = el.offsetParent;
    top += el.offsetTop;
  }

  return (
    top < (window.pageYOffset + window.innerHeight) &&
    (top + height) > window.pageYOffset && (
      top < (window.pageYOffset + window.innerHeight) && top + height <= (window.pageYOffset + window.innerHeight) && top > window.pageYOffset ||
      top <= window.pageYOffset && top + height > (window.pageYOffset + window.innerHeight)
    )
  );
}
const Model = () => {
  const {
    model,
  } = useSelector((state) => state.main);
  const dispatch = useDispatch();
  const { id } = useParams();

  const [form, setForm] = useState({
    date: '',
    feature: '',
    percent: ''
  });

  const navigate = useNavigate();
  const [isError, setIsError] = useState(false);
  const charts = useMemo(() => {
    return model.charts?.map((chart) => ({
      ...chart,
      feature: chart.feature?.replaceAll("_", ". ").replaceAll(". .", ".")
    }));
  }, [model]);
  const [isLoading, setIsLoading] = useState(false);
  const [targetTab, setTargetTab] = useState(tabs.terms);
  const targetTabs = useMemo(() => {
    if (!charts) {
      return [];
    }

    setTargetTab({ label: 'Важность фич', id: 'tab1' })

    window.targetTabs = [
      { label: 'Важность фич', id: 'tab1' },
      ...charts?.map((chart, index) => ({
        label: `${chart.feature.slice(0, 8)}...`, id: `tab${index + 2}`
      }))
    ];

    return [
      { label: 'Важность фич', id: 'tab1' },
      ...charts?.map((chart, index) => ({
        label: `${chart.feature.slice(0, 8)}...`, id: `tab${index + 2}`
      }))
    ];
  }, [charts]);

  // const downloadTxtFile = useCallback(() => {
  //   const makeTextFile = function (text) {
  //     const blob = new Blob([text], {type: 'text/plain'});
  //     const url = URL.createObjectURL(blob);
  //     const a = document.createElement('a');
  //     a.href = url;
  //     a.download = `#${id}` || 'download';
  //     a.click();
  //   };
  //
  //   let text = `эконометрической модели`;
  //
  //   let terms = ''
  //
  //   for (const term of summary.terms) {
  //     terms += `${term.name.toUpperCase()} - ${term.definition}\n\n`;
  //   }
  //
  //   const summaryText = summary.summary;
  //   const trans = summary.transcription;
  //
  //   text = text.replace('terms', terms).replace('summary', summaryText).replace('trans', trans);
  //
  //   makeTextFile(text)
  // }, [id, model]);

  const onMainPageClick = useCallback(() => {
    navigate(routes.main);
  }, []);

  useLayoutEffect(() => {
    if (!getSummariesHistory().includes(id)) {
      setSummariesHistory([...getSummariesHistory(), id])
    }

    if (id !== undefined) {
      dispatch(loadModel(id))
        .catch((err) => {
          console.log(JSON.stringify(err));
          setIsError(true);
        });
    }
  }, []);

  const onTabChange = useCallback(async (_, value) => {
    const tab = targetTabs.find(({ id }) => value === id);

    const rect = document.getElementById(tab.id).getBoundingClientRect();
    window.scrollTo(0, window.scrollY + (rect.y - 150));
    setTargetTab(tab);
  }, [targetTabs]);

  useEffect(() => {
    return () => {
      eventBus.emit(events.onSummaryExit);
    }
  }, []);

  useEffect(() => {
    if (window.targetTabs?.length) {
      const ids = [...window.targetTabs.map(({ id }) => id)];

      window.onscroll = throttle(() => {
        try {
          for (const id of ids) {
            if (elementInViewport(document.getElementById(id))) {
              const tab = window.targetTabs.find((tab) => id === tab?.id);
              setTargetTab(tab);
              return;
            }
          }
        } catch {}
      }, 10);

      return () => {
        window.onscroll = null;
      }
    }
  }, [targetTabs]);

  const isSubmitDisabled = !form.feature || !form.date || !form.percent;

  const onSubmit = () => {
    setIsLoading(true)
    axios.post(`${API_URL}/api/upload/${id}/recount`, form)
      .finally(() => {
        document.location.reload();
      })
  }

  if (id === undefined || isError) {
    return (
      <Grid>
        <Typography
          fontWeight={'1000'}
          fontSize={'25px'}
          userSelect={'none'}
          fontFamily={'Nunito'}
          color={'var(--hint-color)'}
          mb={'var(--space-md)'}
        >
          Что то пошло не так :( Вернитесь на главную страницу!
        </Typography>
        <Tappable onClick={onMainPageClick}>
          <Grid
            display={'flex'}
            justifyContent={'center'}
            alignItems={'center'}
            borderRadius={'var(--border-radius-sm)'}
            backgroundColor={'var(--bg-color)'}
            p={'10px 5px'}
            border={'1px solid var(--primary-color)'}
          >
            <ArrowBackIosRounded fontSize={'20px'} sx={{ color: 'var(--primary-color)' }} />
            <Typography
              fontWeight={'1000'}
              fontSize={'16px'}
              userSelect={'none'}
              fontFamily={'Nunito'}
              pl={'var(--space-sm)'}
              color={'var(--primary-color)'}
            >
              На главную
            </Typography>
          </Grid>
        </Tappable>
      </Grid>
    )
  }

  return (
    <Grid>
      <Grid className={styles.mobile}>
        <Tappable onClick={onMainPageClick}>
          <Grid
            display={'flex'}
            justifyContent={'center'}
            alignItems={'center'}
            borderRadius={'var(--border-radius-sm)'}
            p={'10px 5px'}
            border={'1px solid var(--primary-color)'}
            mb={'10px'}
          >
            <ArrowBackIosRounded fontSize={'20px'} sx={{ color: 'var(--primary-color)' }} />
            <Typography
              fontWeight={'1000'}
              fontSize={'16px'}
              userSelect={'none'}
              fontFamily={'Nunito'}
              pl={'var(--space-sm)'}
              color={'var(--primary-color)'}
            >
              На главную
            </Typography>
          </Grid>
        </Tappable>
      </Grid>
      <Grid mt={'var(--space-md)'} width={'100%'}>
        <PreloadContentPlacement
          isLoading={model?.isLoading || isLoading}
        >
          <Grid
            zIndex={100}
            position={'sticky'}
            display={'flex'}
            width={'100%'}
            top={0}
            height={'calc(var(--header-height) - 5px)'}
            borderRadius={'var(--border-radius-sm)'}
            pl={'var(--space-sm)'}
            alignItems={'center'}
            style={{ backgroundColor: 'var(--bg-color)', userSelect: 'none', zIndex: 1000000000000 }}
          >
            <Grid pr={'var(--space-md)'} zIndex={1000000000000} className={styles.desktop}>
              <Tappable onClick={onMainPageClick}>
                <Grid
                  display={'flex'}
                  justifyContent={'center'}
                  alignItems={'center'}
                  borderRadius={'var(--border-radius-sm)'}
                  backgroundColor={'var(--bg-color)'}
                  p={'10px 5px'}
                  minWidth={'140px'}
                  border={'1px solid var(--primary-color)'}
                >
                  <ArrowBackIosRounded fontSize={'20px'} sx={{ color: 'var(--primary-color)' }} />
                  <Typography
                    fontWeight={'1000'}
                    fontSize={'16px'}
                    userSelect={'none'}
                    fontFamily={'Nunito'}
                    pl={'var(--space-sm)'}
                    color={'var(--primary-color)'}
                    className={styles.desktop}
                  >
                    На главную
                  </Typography>
                </Grid>
              </Tappable>
            </Grid>
            <Tabs
              value={targetTab?.id}
              onChange={onTabChange}
              aria-label="date-tabs"
              variant="scrollable"
            >
              {targetTabs.map((tab) => (
                <Tab key={tab?.id} label={tab?.label} value={tab?.id} />
              ))}
            </Tabs>
          </Grid>
          <Typography
            fontFamily={'Nunito'}
            fontSize={'32px'}
            lineHeight={1.2}
            userSelect={'none'}
            fontWeight={'bold'}
            color={'var(--text-secondary-color)'}
            mt={'var(--space-md)'}
            mb={'var(--space-md)'}
          >
            Модель #{id}
          </Typography>
          <Grid
            zIndex={100}
            display={'flex'}
            width={'100%'}
            flexDirection={'column'}
            top={0}
            borderRadius={'var(--border-radius-sm)'}
            gap={1}
            p={2}
            mb={3}
            style={{ backgroundColor: 'var(--bg-color)', zIndex: 1000000000000 }}
          >
            <Typography
              fontFamily={'Nunito'}
              fontSize={'22px'}
              lineHeight={1.1}
              userSelect={'none'}
              fontWeight={'bold'}
              mb={2}
              color={'var(--text-secondary-color)'}
            >
              Перестроить график
            </Typography>
            <FormControl fullWidth>
              <InputLabel sx={{ color: 'var(--primary-color) !important' }} id="demo-simple-select-label">Фича</InputLabel>
              <Select
                labelId="demo-simple-select-label"
                id="demo-simple-select"
                value={form.feature}
                label="Фича"
                onChange={(event) => setForm((form) => ({ ...form, feature: event.target.value }))}
              >
                {features.map((feature) => (
                  <MenuItem key={feature} value={feature}>{feature}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel sx={{ color: 'var(--primary-color) !important' }} id="select-date-label">Дата</InputLabel>
              <Select
                labelId="select-date-label"
                id="select-date"
                value={form.date}
                label="Дата"
                onChange={(event) => setForm((form) => ({ ...form, date: event.target.value }))}
              >
                {dates.map((feature) => (
                  <MenuItem key={feature} value={feature}>{feature}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <Input
              type="number"
              label={'Изменить на стоолько процентов'}
              fullWidth
              value={form.percent}
              onChange={(event) => setForm((form) => ({ ...form, percent: event.target.value }))}
            />
            <Button variant={'filled'} disabled={isSubmitDisabled} onClick={onSubmit}>
              Перестроить
            </Button>
          </Grid>
          <div style={{ maxWidth: '100%', overflowX: 'auto' }}>
            <Typography
              fontWeight={'1000'}
              fontSize={'28px'}
              userSelect={'none'}
              fontFamily={'Nunito'}
              color={'white'}
              mb={2}
            >
              Важность фич
            </Typography>
            <div style={{ borderRadius: '20px', overflow: 'auto', background: 'var(--bg-color)' }}>
              <div style={{ width: '760px', transform: 'translateX(-5%)' }} id={'tab1'}>
                <Chart
                  loaderStyle={{ background: 'unset', transform: 'translateX(5%)' }}
                  src={`${process.env.REACT_APP_SERVER_API || ''}/${model.featureWeightsChartLink}`}
                />
              </div>
            </div>
          </div>
          {charts?.map(({ chartLink, feature }, index) => (
            <div style={{ maxWidth: '100%', paddingTop: '52px' }} id={`tab${index + 2}`}>
              <Typography
                fontWeight={'1000'}
                fontSize={'28px'}
                userSelect={'none'}
                fontFamily={'Nunito'}
                color={'white'}
                lineHeight={1.1}
                mb={2}
              >
                {feature}
              </Typography>
              <Chart
                src={`${process.env.REACT_APP_SERVER_API || ''}/${chartLink}`}
              />
            </div>
          ))}
        </PreloadContentPlacement>
      </Grid>
    </Grid>
  );
};

export default Model;