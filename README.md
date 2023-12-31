# Petrovich-Parser-API
Calculation of repair materials

API-сервис по расчёту материалов для ремонта с помощью сайта Petrovich предоставляет возможность получить список материалов в формате JSON на основе выбранного типа помещения и параметров комнаты.

Для использования сервиса необходимо выполнить следующие шаги:

1. Отправить HTTP-запрос к API-сервису, указав тип помещения и параметры комнаты.
2. API-сервис обработает запрос и выполнит расчёт материалов на основе предоставленных данных.
3. В ответ на запрос API-сервис вернёт список материалов в формате JSON.


### Сделать расчёт материалов

Отправить POST-запрос на адрес `/` и заполнить все поля.

Пример запроса:

```json
{
  "type_room": "Кухня-гостиная",
  "length": "2",
  "width": "3",
  "height": "2"
}
```
Пример ответа:

```json
[
    {   
        "type": "Кухня-гостиная",
        "materials": [
            {
                "name": "Пол",
                "type": "Черновые",
                "products": [
                    {
                        "amount": "10",
                        "article": "502673",
                        "brand": "",
                        "description": "Ровнитель для пола универсальный предназначен для выравнивания и корректирования бетонных и монолитных цементных и полимер-гипсовых стяжек, в жилых помещениях под укладку напольной керамической плитки, выстилающих покрытий, паркета и для применения в системе «теплый пол». Нанесенный раствор не оставлять длительное время без напольного покрытия. ",
                        "img": "https://cs.petrovich.ru/image/13123436/original-600x600-fit.jpg",
                        "logo": "https://cs.petrovich.ru/image/13123436/original-65x65-fit.jpg",
                        "name": "Ровнитель (наливной пол) универсальный КМ Юниверсум самовыравнивающийся 20 кг",
                        "price": "464",
                        "summ": "4640",
                        "type": "Ровнитель",
                        "url": "https://petrovich.ru/product/502673/"
                    }
                ]
            },
            {
                "name": "Стены",
                "type": "Черновые",
                "products": [
                    {
                        "amount": "10",
                        "article": "161079",
                        "brand": "",
                        "description": "Сухая штукатурная смесь для профессионального машинного нанесения на основе гипсового вяжущего и легкого заполнителя с применением минеральных и химических добавок, обеспечивающих высокую адгезию, водоудерживающую способность и оптимальное время работы. Предназначена для выполнения внутренних однослойных гипсовых штукатурок на потолках и стенах с помощью штукатурного агрегата, а также для доведения поверхности до глянца без дополнительного шпаклевания перед нанесением декоративных покрытий (красок, декоративных составов, обоев и т.п.) Для Москвы и Твери поставляется мешок серого цвета (внутри цвет серый). Для СПБ и СЗФО мешок синего цвета (внутри цвет светлый).",
                        "img": "https://cs.petrovich.ru/image/6184509/original-600x600-fit.jpg",
                        "logo": "https://cs.petrovich.ru/image/6184509/original-65x65-fit.jpg",
                        "name": "Штукатурка гипсовая Волма Гипс Актив МН 30 кг",
                        "price": "535",
                        "summ": "5350",
                        "type": "Штукатурка",
                        "url": "https://petrovich.ru/product/161079/"
                    },
                    {
                        "amount": "7",
                        "article": "631141",
                        "brand": "",
                        "description": "Предназначен для использования в качестве опорной направляющей при оштукатуривании и выравнивании полов для получения ровной поверхности. Изготовлен из оцинкованной стали толщиной 0,60 мм. Если иное не предусмотрено проектом, по завершении штукатурных работ маяки необходимо удалить и восстановить целостность поверхности тем же штукатурным составом. (Согласно своду правил 71.13330.2017 Изоляционные и отделочные покрытия. Актуализированная редакция СНиП 3.04.01-87 (с Изменением N 1) п 7.2.11)",
                        "img": "https://cs.petrovich.ru/image/5771160/original-600x600-fit.jpg",
                        "logo": "https://cs.petrovich.ru/image/5771160/original-65x65-fit.jpg",
                        "name": "Профиль маячковый КМ Эксперт 6 мм 3 м 0,60 мм оцинкованный",
                        "price": "163",
                        "summ": "1141",
                        "type": "Профиль маячок",
                        "url": "https://petrovich.ru/product/631141/"
                    },
                    {
                        "amount": "1",
                        "article": "131587",
                        "brand": "",
                        "description": "Предназначены для крепления профилей маячков 6 мм и 10 мм при выравнивании стен и полов. Изготовлены из пластмассы.",
                        "img": "https://cs.petrovich.ru/images/1240107/original-600x600-fit.jpg",
                        "logo": "https://cs.petrovich.ru/images/1240107/original-65x65-fit.jpg",
                        "name": "Крепления для профилей маячков 6 мм и 10 мм универсальные (100 шт.)",
                        "price": "479",
                        "summ": "479",
                        "type": "Крепления для профилей маячков",
                        "url": "https://petrovich.ru/product/131587/"
                    }
                ]
            },
            {
                "name": "Потолок",
                "type": "Черновые",
                "products": [
                    {
                        "amount": "2",
                        "article": "687852",
                        "brand": "",
                        "description": "Финишная шпаклевка белого цвета на полимерном связующем, предназначена для тонкослойного шпатлевания стен и потолков во внутренних помещениях с нормальной влажностью. Образует после высыхания белую, плотную поверхность. Применяется для выравнивания и устранения дефектов оснований и подготовки их к последующей высококачественной окраске или оклейке обоями. ",
                        "img": "https://cs.petrovich.ru/image/27759545/original-600x600-fit.jpg",
                        "logo": "https://cs.petrovich.ru/image/27759545/original-65x65-fit.jpg",
                        "name": "Шпаклевка полимерная КМ Полимер для сухих помещений белая 20 кг",
                        "price": "751",
                        "summ": "1502",
                        "type": "КМ",
                        "url": "https://petrovich.ru/product/687852/"
                    },
                    {
                        "amount": "1",
                        "article": "104159",
                        "brand": "",
                        "description": "Концентрированный глубоко проникающий (до 5 мм) состав. Предназначен для укрепления поверхностных слоев основания, повышает износостойкость, снижает впитывающую способность основания, обеспыливает поверхность, повышает адгезию. Предотвращает отток воды из растворных смесей, предотвращает появление трещин (при добавлении в сухие смеси) и уменьшает расход краски в процессе финишной отделки. Наносится на бетон, железобетон, штукатурки, плиты из гипса и гипсокартон, кирпич и асбестоцемент, ячеистые бетоны, слегка пачкающиеся, мелящие, но прочно держащиеся покрытия. При многослойном нанесении (2-3 слоя) может использоваться в качестве самостоятельного покрытия по декоративным минеральным основаниям, в т.ч. по искусственному камню, что предполагает возможность влажной очистки обработанной поверхности, в т.ч. с применением моющих средств. Может применяться для консервации на зимний период систем утепления фасадов с тонким штукатурным слоем на стадии базового армированного слоя или декоративной минеральной штукатурки. Для внутренних и наружных работ. ",
                        "img": "https://cs.petrovich.ru/images/2945450/original-600x600-fit.jpg",
                        "logo": "https://cs.petrovich.ru/images/2945450/original-65x65-fit.jpg",
                        "name": "Грунт Крепс 1 л концентрат 1:5",
                        "price": "218",
                        "summ": "218",
                        "type": "Грунт",
                        "url": "https://petrovich.ru/product/104159/"
                    }
                ]
            }
        ]
    }
]
```

### Как запустить проект:

#### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/krivse/Petrovich-Parser-API.git
```

#### Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
# для OS Lunix и MacOS
source venv/bin/activate

# для OS Windows
source venv/Scripts/activate
```

#### Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```


#### Запустить проект:

```
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

###### Автор - Иван Красников, 2023
