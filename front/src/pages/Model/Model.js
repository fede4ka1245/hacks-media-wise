import React, {useCallback, useEffect, useLayoutEffect, useMemo, useState} from 'react';
import PreloadContentPlacement from "../../components/preloadContentPlacement/PreloadContentPlacement";
import {Grid, Typography} from "@mui/material";
import Tabs from "../../ui/tabs/Tabs";
import Tab from "../../ui/tab/Tab";
import Tappable from "../../ui/tappable/Tappable";
import { ArrowBackIosRounded} from "@mui/icons-material";
import {useNavigate, useParams} from "react-router-dom";
import {routes} from "../../routes";
import {useDispatch, useSelector} from "react-redux";
import {loadModel} from "../../store";
import {throttle} from "lodash";
import styles from './Model.module.css';
import {eventBus, events, getSummariesHistory, setSummariesHistory} from "../../logic";
import Button from "../../ui/button/Button";

const tabs = {
}

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

  const [targetTab, setTargetTab] = useState(tabs.terms);
  const targetTabs = useMemo(() => {
    return Object.values(tabs);
  }, []);
  const navigate = useNavigate();
  const [isError, setIsError] = useState(false);

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
    const tab = Object.values(tabs).find(({ id }) => value === id);

    const rect = document.getElementById(tab.id).getBoundingClientRect();
    window.scrollTo(0, window.scrollY + (rect.y - 150));
    setTargetTab(tab);
  }, []);

  useEffect(() => {
    return () => {
      eventBus.emit(events.onSummaryExit);
    }
  }, []);

  useEffect(() => {
    if (tabs.length) {
      const ids = [...Object.values(tabs).map(({ id }) => id)];

      window.onscroll = throttle(() => {
        try {
          for (const id of ids) {
            if (elementInViewport(document.getElementById(id))) {
              const tab = Object.values(tabs).find((tab) => id === tab?.id);
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
  }, []);

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
      <Typography
        fontFamily={'Nunito'}
        fontSize={'24px'}
        lineHeight={1.2}
        userSelect={'none'}
        color={'var(--text-secondary-color)'}
        mt={'var(--space-md)'}
        mb={'var(--space-md)'}
      >
        ID эконометрической модели: {id} <br/>
        Вы можете вернуться к ней с главной страницы.
      </Typography>
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
        style={{ backgroundColor: 'var(--bg-color)', userSelect: 'none', zIndex: 100 }}
      >
        <Grid pr={'var(--space-md)'} className={styles.desktop}>
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
                className={styles.desktop}
              >
                На главную
              </Typography>
            </Grid>
          </Tappable>
        </Grid>
        {/*<Tabs*/}
        {/*  value={targetTab.id}*/}
        {/*  onChange={onTabChange}*/}
        {/*  aria-label="date-tabs"*/}
        {/*  variant="scrollable"*/}
        {/*>*/}
        {/*  {targetTabs.map((tab) => (*/}
        {/*    <Tab key={tab.id} label={tab.label} value={tab.id} />*/}
        {/*  ))}*/}
        {/*</Tabs>*/}
      </Grid>
      <Grid mt={'var(--space-md)'} width={'100%'}>
        <PreloadContentPlacement
          isLoading={model?.isLoading}
        >
          {model.charts?.map(({ chartLink, feature }) => (
            <div>
              <Typography
                fontWeight={'1000'}
                fontSize={'28px'}
                userSelect={'none'}
                fontFamily={'Nunito'}
                color={'white'}
              >
                {feature}
              </Typography>
              <iframe
                src={`${process.env.REACT_APP_SERVER_API}/${chartLink}`}
              />
            </div>
          ))}
        </PreloadContentPlacement>
      </Grid>
    </Grid>
  );
};

export default Model;