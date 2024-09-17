# pyside6-emoji-art
<p>EmojiArt — это интерактивная GUI-программа, разработанная на Python с использованием библиотеки PySide6.</p>
</p>Программа реализует возможность удобного создания анимации для текстовых эмодзи.</p>

<h1>🎨 Дизайн-макет из Figma</h1>

<h2> UX карта версии 1.0 </h2>

![UX map](https://github.com/user-attachments/assets/3fc3cf9a-b1bd-4783-81fa-db63886bbd35)

<h2> Ссылки на макет </h2>

- [Макет](https://www.figma.com/design/4jU9bAvQlci75eTvIVpYV2/Emoji-art?node-id=0-1&t=B5VL2LBED56n34qr-1)
- [Интерактивный макет](https://www.figma.com/proto/4jU9bAvQlci75eTvIVpYV2/Emoji-art?node-id=0-1&t=B5VL2LBED56n34qr-1)


<h1>🛠️ EmojiArt - программа </h1>

<h4> Рабочая область: </h4>

- [ViewWorkSpace](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/views/ViewWorkspace.py)

<h4> Верхняя панель компонентов: </h4>

- Рабочая область [ArtBoard](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentArtBoard.py)
- Список эмодзи быстрого доступа [Store](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentEmojiStore.py)
- Список последних использованных эмодзи [History](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentEmojiHistory.py)

<h4> Нижняя панель компонентов: </h4>

- Карусель фреймов [CarouselOfImages](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentCarouselOfImages.py)
- Список горячих клавиш [Shortcuts](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentShortcuts.py)

<h4> Остальные компоненты: </h4>

- Компонент toast уведомления [ToastMessage](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentToastMessage.py)
- Компонент label уведомления о пустующем виджете (отсутствуют элементы в контейнере) [LabelNotificaion](https://github.com/bonkibon-education/pyside6-emoji-art/blob/main/src/components/ComponentLabelNotification.py)

![emoji-art](https://github.com/user-attachments/assets/54ab073e-50c7-447b-9f6e-935bbbb5c67c)

<h1> 🎚️ Scrollbar </h1>

![scrollbar-menu](https://github.com/user-attachments/assets/a0264ee9-2201-4534-9589-fb84c0e22a3b)


![gif-scrollbar](https://github.com/user-attachments/assets/7e2d2857-7e5c-426a-94bf-3e770d7a0cce)


<h1> 📚 EmojiStore / EmojiHistory </h1>

- EmojiStore — это компонент, который представляет собой список эмодзи. Нажатие левой кнопкой мыши по выбранному пользователем эмодзи перемещает его в буфер обмена.

- EmojiHistory - это компонент, который служит для отображения истории использованных эмодзи. Этот компонент позволяет пользователям легко отслеживать и повторно использовать недавно задействованные эмодзи.

![gif-store](https://github.com/user-attachments/assets/df80efdc-0a27-40c4-a611-56a086588f54)

<h1> 📅 ArtBoard </h1>

ArtBoard - это компонент, который предоставляет пользователю табличное пространство для размещения эмодзи. ArtBoard поддерживает функции:
- редактирование;
- очистка таблицы;
- изменение размеров;
- копирование, вставка, удаление эмодзи. 

<h2> Пример арта </h2>

![gif-art-board-1](https://github.com/user-attachments/assets/8201e59e-d39d-40e6-bfdb-d61da204b26b)

<h2> Правильное и не правильное значение ячейки </h2>

![gif-art-board-validation-cell](https://github.com/user-attachments/assets/f76b01d3-0207-437c-bd8a-fe02561b7f16)

<h2> ArtBoard меню </h2>

Меню открывается на правую кнопку мыши и реализует функционал:
- выделение ячеек;
- копирование эмодзи из выделенных ячеек;
- вставка эмодзи в выделенные ячейки;
- удаление эмодзи из выделенных ячеек;
- изменение размеров ArtBoard.

![art-board-menu](https://github.com/user-attachments/assets/e430b3c4-7377-42ac-a31d-5c195d27cff5)

![gif-art-board-2](https://github.com/user-attachments/assets/03d7897c-b243-469d-a4d6-11fbb0ec2b2b)

<h1>🖼️ CarouselOfImages </h1>

CarouselOfImages - это компонент, который предоставляет пользователю возможность взаимодействовать с сохраненными фреймами:
- режим редактирования по нажатию левой кнопкой мыши;
- дублирование фрейма по нажатию правой кнопкой мыши;
- удаление по нажатию на кнопку "del".

![gif-art-board-frames](https://github.com/user-attachments/assets/adddccec-b106-4e78-9af5-3322b96b321f)

<h1>⌨️ Shortcuts </h1>

Shortcuts - это компонент, который предоставляет пользователю список комбинациий горячих клавиш:

![image 1](https://github.com/user-attachments/assets/ede72766-4521-4a1b-9c1c-be8fa1627ea6)

![image 2](https://github.com/user-attachments/assets/e367406e-9019-4e6c-9a33-a2a29864e2cc)

![image 3](https://github.com/user-attachments/assets/cc93f32e-ccc1-4caf-a335-af7bde7ce226)

![image 4](https://github.com/user-attachments/assets/4414a9dc-169e-4f03-9f4e-d27457fd0695)

![image 5](https://github.com/user-attachments/assets/65a343f5-e554-4166-bc34-c3dd747f301c)


<h1>💾 Сохранение анимации </h1>

Сохранение анимации доступно с помощью комбинации клавиш. Анимация эскпортируется в формат .json ([Пример](https://github.com/bonkibon-education/pyside6-emoji-art/tree/main/example))
