# hackaton-yandex-market-packing
[![YM-pack workflow](https://github.com/Legyan/hackathon-yandex-market-packing/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/Legyan/hackathon-yandex-market-packing/actions/workflows/main.yml)

Развёрнутый проект доступен по адресу http://62.84.121.232.

Swagger документация backend: http://62.84.121.232:8000/docs.

Swagger документация DS: http://62.84.121.232:8001/docs.

[Github Pages](https://legyan.github.io/hackathon-yandex-market-packing/)


### Стек технологий 

![](https://img.shields.io/badge/Python-3.10-black?style=flat&logo=python) 
![](https://img.shields.io/badge/FastAPI-0.96.0-black?style=flat&logo=fastapi)
![](https://img.shields.io/badge/Uvicorn-0.17.0-black?style=flat&logo=uvicorn)
![](https://img.shields.io/badge/Pydantic-1.10.8-black?style=flat)
![](https://img.shields.io/badge/SQLAlchemy-1.4.36-black?style=flat)
![](https://img.shields.io/badge/Pandas-2.0.2-black?style=flat&logo=pandas)
![](https://img.shields.io/badge/Numpy-1.24.3-black?style=flat&logo=numpy)
![](https://img.shields.io/badge/LightGBM-3.3.5-black?style=flat&logo=lightgbm)
![](https://img.shields.io/badge/Typing-3.7.4.3-black?style=flat&logo=typing)
![](https://img.shields.io/badge/React-18.2.0-black?style=flat&logo=react)
![](https://img.shields.io/badge/TypeScript-4.9.5-black?style=flat&logo=typescript)
![](https://img.shields.io/badge/Redux-4.2.1-black?style=flat&logo=redux)
![](https://img.shields.io/badge/Docker-black?style=flat&logo=docker)

# Проект для Хакатона Яндекс Маркета по рекомендации упаковки для заказа

Проект разработан командой №10 в рамках хакатона с целью определения оптимального типа упаковки товаров и предоставления данной информации специалистам по упаковке в Яндекс Маркете.

В целях сохранения целостности доставляемого покупателю товара, часть посылок отправляется в упаковках. 
Специалисты Яндекс Маркета обратили внимание, что сотрудник склада затрачивает значительное количество времени на выбор упаковочного материала, а также часто совершает не оптимальный с точки зрения экономики выбор. 
Основной задачей проекта является поиск и реализация способа передачи пользователю рекомендации о выборе упаковочного материала.

### Цели нашего проекта:
•	с высокой точностью рекомендовать правильную упаковку для заказа, которая позволит доставить товары без порчи клиенту и минимизирует затраты на упаковочный материал;

•	создание интерфейса, понятного новым сотрудникам при этом полезного  и не обременяющего опытных специалистов.

•	отображение статистики о работе модели;

### JTBD подход и общая идея:
•	Когда я выбираю упаковку, хочу доступные, понятные и наглядные рекомендации, чтобы не тратить много времени на изучение функционала

•	Когда я упаковываю товар, хочу выбирать из готовых элементов, чтобы не обращаться к бригадирам и закрывать смену быстрее

•	Когда я упаковываю товар, хочу иметь пул шаблонов для разных товаров, чтобы поддерживать качество упаковки и быстрее отправлять упакованный товар

•	Когда я упаковываю товар, хочу предварительно посмотреть на готовый результат, чтобы избежать ошибок

•	Когда я упаковываю товар, хочу иметь доступ к изменению товара и самой упаковки, чтобы иметь возможность выбирать самому упаковку и убирать ненужный товар из упаковки

•	Когда я точно знаю какая  упаковка нужна, я не хочу тратить время на просмотр  не нужных экранов и нажатие лишних кнопок

### Требования к интерфейсу:
• Должен отображать содержимое заказа для контроля комплектности.

• Должен на основании содержимого заказа, подсказывать упаковщику в какую тару (коробку, пакет, с учетом размера) нужно упаковать заказ.

•	Должен быть интуитивно понятен новым сотрудникам

•	Не должен содержать дополнительных действий для опытных сотрудников 

•	Должен отображать информацию необходимость в дополнительной упаковке для хрупких товаров и другие подсказки

•	Должен учитывать все сценарии работы сотрудника склада

• Должен соответствовать фирменному стилю Заказчика


### Итоговый концепт:
   Система предлагает готовые варианты упаковщику. Есть готовые рекомендации и целые комбинации упаковок, но при этом можно выбирать свой вариант упаковки с помощью скана штрихкода своей упаковки и редактировать наполнение упаковки с помощью кнопки "изменить состав коробки".  Прежде чем отправить упаковку можно предварительно посмотреть финальный результат сборки упаковки и изменить ее состав. Предусмотрены краевые сценарии с бракованными и отсутствующими заказами, проблемами оборудования упаковщика. 

<details open>
<summary><h2>Описание алгоритма выбора упаковки заказа</h2></summary>
   
### Данные

В нашем распоряжении историческая информация о заказанных товарах и упаковке, представленая в $6$ таблицах.
По количеству товаров в составе заказы распределены неравномерно. 65 % из них с одним товаром, а 97 % всех заказов включают в себя не более 5 товаров.

![1](https://github.com/Legyan/hackathon-yandex-market-packing/assets/93463677/e19bc315-ab4e-4528-a91d-03793bcbf915)

Практически все заказы помещаются в одну упаковку (без учета товаров, не требующих упаковки или упакованных в пленку).

![2](https://github.com/Legyan/hackathon-yandex-market-packing/assets/93463677/6dd94c34-3874-44e5-be05-d624e036da67)

Покрытие потребности заказчика при предсказании упаковки для заказов, включающих не более $5$ товаров, составляет $93.79$ %.

![3](https://github.com/Legyan/hackathon-yandex-market-packing/assets/93463677/e9ad4950-b351-41f6-95df-9a07ef2a4872)

### Алгоритм
Предсказание упаковки можно разделить на $3$ основные части:
1. Выделение товаров не требующих упаковки или упаковываемых в пленку на основе карготипов $340$ и $360$;
2. Подбор упаковки для одного товара на основе накопленной статистики и с помощью сравнения габаритов товара с габаритами имеющихся упаковок. Предлагается самая дешевая из подошедших упаковок и, по возможности, еще 1-2 альтернативы.

![4png](https://github.com/Legyan/hackathon-yandex-market-packing/assets/93463677/b1ef2818-364a-43f7-9782-c8ad5d73c71c)

3. ML-подход для заказов с 2-5 товарами. Предлагается $3$ самые вероятные по мнению модели варианта упаковки.

### Результаты
Для $76.7$ % заказов алгоритм предсказывает подходящую и оптимальную по цене упаковку.
Экономия на упаковке составила $209$ $771.49$ руб. или $9.56$ %. Если считать, что в нашем распоряжении были данные за один день и распределение заказов в среднем соответствует датасету, то за год экономия может составить $76.5$ млн. руб.

![5](https://github.com/Legyan/hackathon-yandex-market-packing/assets/93463677/5f517a30-fa32-4eb0-9ac6-2e8ccdc95e6f)

</details>

<details open>
<summary><h2>Описание работы проекта</h2></summary>

Сценарии работы и интерфейс пользователя приведены по [ссылке](https://www.figma.com/file/s6KACisVHbtIxQuGz2uyrj/IDEA-3-June-2023-Hackathon?type=design&node-id=0-1&t=YsuUFWT93T5hKbSs-0).

При первом переходе на сайт сервиса, пользователь попадает на страницу регистрации стола. Список доступных для ввода столов приведён в [tables.csv](./backend/data/tables.csv) в столбце name. Введите любой, например `PACK-1`, и нажмите Enter. Пользователь будет авторизован в системе, ему вернётся JWT токен и присвоится выбранный стол.

Далее пользователь попадает на страницу регистрации принтера. Список доступных для ввода принтеров приведён в [printers.csv](./backend/data/printers.csv) в столбце name. Введите любой, например `001`, и нажмите Enter. Пользователю будет присвоен выбранный принтер.

После регистрации принтера пользователь попадает на стартовую страницу сервиса. Здесь отображается его статистика и есть возможность взять заказ, закрыть стол (logout) и сообщить о проблеме. Нажмите кнопку "Получить заказ". По нажатию кнопки пользователь получает заказ из сохранённых в базе.

*Заказы добавляются в базу с помощью POST запроса на эндпоинт [api/v1/order](http://localhost:8000/docs#/Orders/add_order_api_v1_order_post). Отправляя в запросе список существующих в [базе](./backend/data/products.csv) SKU или взяв готовый JSON заказа из [тестовых заказов](./backend/data/orders.json), вы можете добавить новый заказ в базу. Перед отправлением заказа пользователю, по специальному [эндпоинту](http://localhost:8001/docs#/default/get_prediction_pack_post) для него будут получены и записаны в базу данных рекомендации по упаковке. На момент начала проверки в базе данных уже лежит информация о 5-ти тестовых заказах, добавленных в базу managment командой пункте 7 инструкции по запуску проекта.*

После получения заказа, у пользователя на экране отображаются товары в заказе и несколько рекомендаций по их упаковке. Переключая рекомендованные варианты упаковки в правой части экрана, в левой части экрана пользователь может видеть какие товары в какую коробку рекомендовал упаковать алгоритм.

Выбрав одну из рекомендаций, пользователь сканирует или вводит вручную коробку, в которую будет упаковывать товар. Нажмите кнопку "Ввести с клавиатуры", введите название одной из отображенных на экране [упаковок](./backend/data/cartontypes.csv) и нажмите Enter. Выбранная упаковка отобразится на экране.

После открытия коробки, пользователь сканирует или вводит вручную штрих-код товара, sku которого отображён рядом с количеством товара в упаковке. Введите любой штрих-код из [таблицы](./backend/data/barcode_sku.csv)(столбец barcode), значение столбца SKU которого совпадает с SKU одного из товаров в активной коробке, и нажмите Enter. Например, для SKU `d9af6ce6f9e303f4b1a8cb47cde21975` можно ввести штрих-код `44333105202301`. После введения штрих-кода с помощью кнопки "Ввести с клавиатуры", его состояние отобразится в интерфейсе пользователя.

После отправки штрих-кода, сервис может потребовать предоставить IMEI и/или маркировку "Честный знак". Их полноценная проверка в проекте не реализуется, для прохождения mock-проверки введите любую 15-символьную строку для IMEI и 13-ти символьную строку для "Честного знака".

После заполнения упаковки пользователь её закрывает и печатает для неё штрих-код. Нажмите на кнопку "Закрыть коробку" рядом с иконкой заполненной коробки. В правом верхнем углу отобразится окно с предложением распечатать штрих-код, нажмите "Печатать". Закрытие коробки отобразится на экране.

При несоответствии действий пользователя выбранной рекомендации, пользователь будет переключен в режим самостоятельной сборки.В этом режиме рекомендации не отображаются, но действия пользователя также отображаются на экране и записываются в базу данных. 

Если пользователю будет необходимо убрать уже отсканированный товар из коробки, он может это сделать с помощью кнопки "Изменить состав коробки". Рядом с товарами в коробке отобразятся красные "крестики" по нажатию которых можно будет выбрать несколько товаров для удаления. После того как все товары для удаления отмечены, пользователь нажимает кнопку "Готово", и товары "вываливаются" из коробки, переставая считаться отсканированными. Они отображаются под упаковками в левой части экрана и могут быть помещены в другую упаковку.

Если во время упаковки заказа у пользователя возникла проблема, он может сообщить о ней нажав на кнопку "Есть проблема". Нажмите на эту кнопку, на экране отобразятся кнопки с возможными проблемами, нажав на которые, пользователь может сообщить об отсутствии товара, бракованном товаре в заказе или вызвать на помощь бригадира при более сложной проблеме.

После того как пользователь упаковал все товары в заказе и закрыл все упаковки, он нажимает на кнопку "Упаковано". Если все товары из заказа действительно были упакованы, он попадает на экран "Хорошая работа" с кнопкой "Готово". По нажатию на эту кнопку, пользователь попадает на экран получения нового заказа для упаковки со своей обновлённой статистикой сборки заказов.

Далее пользователь может получить новый заказ, или закончить работу. Для завершения работы пользователь нажимает на кнопку "Закрыть стол" на экране получения нового заказа, от него отвязывается занятый им стол и принтер и сервис возвращется на стартовую страницу регистрации стола.

</details>

<details open>
<summary><h2>Запуск проекта</h2></summary>

1. Перейти в директорию /infra:

    ```shell
    cd infra/
    ```

2. Создать в директории файл .env и заполнить его согласно примеру в .env.example:

    ```shell
   nano .env
   ```

   ```
    POSTGRES_DB=ym-packing
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db-ym-pack
    DB_PORT=5432
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@db-ym-pack/postgres
    DS_PACK_URL=http://ds-ym-pack:8000/pack
    SECRET_KEY=SECRET_KEY
   ```

3. Запустить все контейнеры приложения с помощью Docker-compose:

    ```shell
    sudo docker-compose up -d --build
    ```

4. Применить миграции к базе данных.

   ```shell
   sudo docker exec infra_backend-ym-pack_1 alembic upgrade head
   ```

5. Заполнить базу данных тестовыми данными:

    ```shell
    sudo docker exec infra_backend-ym-pack_1 python3 -m app.management.fill_db
    ```

6. Сгенерировать штрих-коды товаров и добавить в базу:

    ```shell
    sudo docker exec infra_backend-ym-pack_1 python3 -m app.management.add_random_barcodes
    ```

7. Добавить тестовые заказы:

    ```shell
    sudo docker exec infra_backend-ym-pack_1 python3 -m app.management.add_orders
    ```

Проект будет развернут и доступен по адресу http://localhost.

Swagger документация backend: http://localhost:8000/docs.

Swagger документация DS: http://localhost:8001/docs.

Для обнуления базы данных доступна команда:

```shell
sudo docker exec infra_backend-ym-pack_1 python3 -m app.management.clear_db
```

</details>

<details open>
<summary><h2>ToDo</h2></summary>

### Backend

1. Добавить очередь задачь для получения рекомендаций от контейнера DS.

2. Доделать проверку штрих-кода на то, что товар с sku этого штрих-кода уже был пробит необходимое для этого заказа количество раз.

3. Реализовать хранение и обновление статистики работы пользователя для подсчёта и вывода KPI.

### DS

1. Используемый подход по сравнению диаметра круга раскрытого пакета и диагонали товара-параллелепипеда это частный случай эллипса, описывающего прямоугольник. Можно усложнить расчеты, подбирая эллипс и сравнивая его длину с длиной окружности пакета. Скорее всего, с таким подходом пакеты будут предсказаны еще точнее;
2. Опытным путем подобрать коэффициенты увеличения длины и диагонали меньшей грани товара (вместо предложенных $10$ % и $20$ %) для его комфортной и быстрой упаковки;
3. Определить случаи, требующие упаковку товара только в пакет или только в коробку по карготипам и добавить соответствующие условия в алгоритм;
4. Увеличить датасет для заказов с 2-5 товарами в составе и обучить модели отдельно для каждого количества товаров;
5. После увеличения датасета добавить новые признаки на основе характеристик товаров: площадь каждой из трех разных граней, диагонали граней, среднее линейное измерение ((a+b+c)/3), максимальное и минимальное лиейное измерение, максимальные, минимальные, средние и общие вес и объем. На датасете в $30$ тыс. заказов увеличение метрики f1_micro было незначительным - лишь на $0,01$ (и это на $20$% всех заказов), поэтому мы не стали добавлять это признаки в модель. На большом количестве данных и разных моделях под каждое количество товаров в заказе этот подход может дать результаты;
6. Для ml подхода определить самые важные карготипы и также добавить их в качестве новых признаков. На текущих данных ohe-векторы карготипов не дали никакого результата и только усложнили вычисления, поэтому мы не стали оставлять их в финальной версии ml-алгоритма.
   
### Design
1. Поиск и проработка новых краевых сценариев;
   
</details>

## Команда

*Project manager*

- [Максим Евдокимов]() 

*Design*

- [Евгения Швецова]()

- [Ксения Забровская]()

*Data Science*

- [Татьяна Кубарь](https://github.com/TaniaKubar)

- [Дмитрий Лялин](https://github.com/Aalfaa)

- [Иван Марков]()

*Frontend*

- [Алексей Шайдуллин](https://github.com/AlekseyShaydullin)

- [Владислав Никитин](https://github.com/BeRealDude)

*Backend*

- [Левон Гегамян](https://github.com/Legyan)

- [Никита Макарьев](https://github.com/NikitaMackariev)
