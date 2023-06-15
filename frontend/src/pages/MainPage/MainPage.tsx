import { FC } from 'react';
import style from './MainPage.module.css'
import Progressbar from '../../components/Progressbar/Progressbar';
import Footer from '../../components/Footer/Footer';
import box from '../../images/icon_stat_box.svg';
import speed from '../../images/icon_speedstat.svg';
import cup from '../../images/icon_cup.svg';
import ButtonLink from '../../components/ui/ButtonLink/ButtonLink';
import { useSelector } from '../../utils/type/redux';
import ButtonForm from '../../components/ui/ButtonForm/ButtonForm';
import { getCookie } from '../../utils/cookie';

const MainPage: FC = () => {
  const user = useSelector(store => store.userInfo);

  console.log(user);


  return (
    <>
      <section className={style.wrapper}>
        <div className={style.btnsWrapper}>
          <ButtonLink
            purpose={'problem'}
            title={'Есть проблема'}
            link={'/problems'}
          />
          <ButtonLink
            purpose={'logout'}
            title={'Закрыть стол'}
            link={'/table'}
          />
        </div>
        <div className={style.statWrapper}>
          <Progressbar title={'Упаковка'} />
          <ul className={style.statistics}>
            <li className={style.stat}>
              <h3 className={style.statTitle}>Упаковано за сегодня</h3>
              <img src={box} className={style.img} alt='Иконка коробки' />
              <p className={style.description}>Количество упакованного товара</p>
              <span className={style.counter}>12</span>
            </li>
            <li className={style.stat}>
              <h3 className={style.statTitle}>Скорость работы</h3>
              <img src={speed} className={style.img} alt='Иконка спидометр' />
              <p className={style.description}>Количество упаковок в день</p>
              <span className={style.counter}>156</span>
            </li>
            <li className={style.stat}>
              <h3 className={style.statTitle}>Сверхзадачи</h3>
              <img src={cup} className={style.img} alt='Иконка кубка' />
              <p className={style.description}>Упаковки товара сверхнормы</p>
              <span className={style.counter}>11</span>
            </li>
          </ul>
        </div>
        <ButtonForm purpose={'package'} text={'Получить заказ'} />
      </section>
      <Footer />
    </>
  )
}

export default MainPage;
