var services = [
    {
        "name": "Чистка пальто",
        "type": "Верхняя одежда",
        "branch": "Центральный",
        "prices": [1500, 1650, 1800]
    },
    {
        "name": "Чистка костюма",
        "type": "Деловая одежда",
        "branch": "Северный",
        "prices": [1100, 1200, 1350]
    },
    {
        "name": "Выведение пятен",
        "type": "Спецобработка",
        "branch": "Центральный",
        "prices": [600, 900, 1200]
    },
    {
        "name": "Чистка пуховика",
        "type": "Верхняя одежда",
        "branch": "Южный",
        "prices": [1900, 2100, 2300]
    },
    {
        "name": "Чистка свадебного платья",
        "type": "Деликатные ткани",
        "branch": "Центральный",
        "prices": [3500, 4000, 4600]
    },
    {
        "name": "Чистка ковра",
        "type": "Домашний текстиль",
        "branch": "Южный",
        "prices": [950, 1100, 1250]
    }
];

var rpad = function(str, length) {
    // js не поддерживает добавление нужного количества символов
    // справа от строки, т.е. аналога ljust из Python здесь нет
    str = str.toString(); // преобразование в строку
    while (str.length < length)
        str = str + ' '; // добавление пробела в конец строки
    return str; // когда все пробелы добавлены, возвратить строку
};

var printServices = function(items) {
    console.log(
        rpad("Услуга", 26),
        rpad("Тип", 20),
        rpad("Филиал", 14),
        rpad("Стоимость, руб.", 20)
    );
    // был выведен заголовок таблицы
    for (var i = 0; i <= items.length - 1; i++) {
        // в цикле выводится каждая запись
        console.log(
            rpad(items[i]['name'], 26),
            rpad(items[i]['type'], 20),
            rpad(items[i]['branch'], 14),
            rpad(items[i]['prices'], 20)
        );
    }
    console.log('\n'); // добавляется пустая строка в конце вывода
};

// фильтрация по филиалу
var filterByBranch = function(items, group) {
    return items.filter(function(item) {
        return item['branch'] === group;
    });
};

// среднее арифметическое массива чисел
var average = function(values) {
    var sum = values.reduce(function(a, b) { return a + b; }, 0);
    return sum / values.length;
};

// фильтрация по средней стоимости
var filterByAveragePrice = function(items, minAverage) {
    return items.filter(function(item) {
        return average(item['prices']) > minAverage;
    });
};

printServices(services);

var group = prompt("Введите название филиала для фильтрации:");
console.log("Услуги филиала " + group + ":");
printServices(filterByBranch(services, group));

var minAverage = parseFloat(prompt("Введите минимальную среднюю стоимость услуги:"));
console.log("Услуги со средней стоимостью выше " + minAverage + ":");
printServices(filterByAveragePrice(services, minAverage));
