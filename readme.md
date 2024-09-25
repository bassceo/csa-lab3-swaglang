# Лабораторная работа №3. Эксперимент

- **Лукьянчук Ярослав Евгеньевич P3223**
- **Вариант:** asm, risc, harv, mc, instr, binary, stream, port, cstr, prob2

---

## SwagLang


```
<program> ::= <data_section> <text_section>

<data_section> ::= "data:" "{" {<data_definition>}* "}"

<data_definition> ::= <label> ":" <data_value> ";"

<data_value> ::= <string_literal> | <number>

<string_literal> ::= '"' {<char>}* '"'

<number> ::= <digit>+

<text_section> ::= "run" <block>

<block> ::= ":{" {<instruction>}* "}"

<instruction> ::= <label> ":" <block>
               | <label> ":"
               | <command> ";"

<command> ::= "load" "[" <reg> "," <value> "]"
           | "load" "[" <reg> "," "(" <address_from_reg> ")" "]"
           | "store" "[" <reg> "," <address> "]"
           | "store" "[" <reg> "," "(" <address_from_reg> ")" "]"
           | "input" "[" <reg> "," <stream> "]"
           | "output" "[" <reg> "," <stream> "]"
           | "inputchar" "[" <reg> "," <stream> "]"
           | "outputchar" "[" <reg> "," <stream> "]"
           | "add" "[" <reg> "," <reg_or_value> "]"
           | "sub" "[" <reg> "," <reg_or_value> "]"
           | "cmp" "[" <reg> "," <reg_or_value> "]"
           | "jmp" "[" <label> "]"
           | "je" "[" <label> "]"
           | "jn" "[" <label> "]"
           | "mod" "[" <reg> "," <reg_or_value> "]"
           | "stop"

<reg> ::= "R1" | "R2" | "R3"

<value_or_address> ::= <number> | <address>

<address> ::= <label>

<stream> ::= "!" <label>

<label> ::= <letter> [<letter> | <digit>]*

<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

<letter> ::= "a" | ... | "z" | "A" | ... | "Z"

<char> ::= <letter> | <digit> | <special_char>

<special_char> ::= "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "_" | "`" | "{" | "|" | "}" | "~"
```

---

## Команды

### Операции с регистрами и памятью

- `load[reg, value_or_address]`
- `store[reg, address]`
- `store_to[reg, (address_from_reg)]`
- `add[reg, reg]`
- `sub[reg, reg]`
- `cmp[reg, reg]`
- `mod[reg, reg]`


### Ввод и вывод данных

- `input[reg, !stream]`
- `output[reg, !stream]`

### Работа с символами

- `inputchar[reg, !stream]`
- `outputchar[reg, !stream]`

### Переходы и метки

- `jmp[метка]`
- `je[метка]`
- `jn[метка]`
- `stop`

---

## Семантика

### Последовательное выполнение

Команды выполняются последовательно сверху вниз, если поток управления не изменен переходами.

### Переходы

- **Безусловные (jmp):** изменяют поток выполнения без условий.
- **Условные (je, jn):** зависят от результата последней операции АЛУ.

### Циклы

Используются метки и переходы для реализации циклов.

**Пример:**

```asm
run {
    load[R1, 0];
    input[R2, !INPUT];

    loop_start: {
        cmp[R2, 0];
        je[exit_loop];
        add[R1, 1];
        sub[R2, 1];
        jmp[loop_start];
    };

    exit_loop: {
        output[R1, !OUTPUT];
    };
}
```

---

## Области видимости

- **Регистры:** Глобальные, доступны всей программе.
- **Метки:** Глобальные, используются для переходов.
- **Память:** Глобальные переменные из секции данных.

---

## Виды литералов

### Целочисленные

Десятичные числа.

```asm
load[R1, 100];
```

### Строковые

Определяются в секции данных в двойных кавычках.

```asm
data {
    greeting: "Hello, World!";
}
```

### Идентификаторы

- **Метки:** Для переходов.
- **Потоки:** Предшествуют `!`.
- **Переменные:** В секции данных.

```asm
input[R2, !INPUT];
loop_start: { ... }
load[R1, myVar];
```

---


## Организация памяти

* Память данных и команд раздельна (harv)
* Размер машинного слова данных 23 бита
 Размер машинного слова адреса 23 бита
* Инструкции хранятся в памяти последовательно.

Память команд


```text
+------------------------------+
| 0        program             |
| 1        program             |
|      ...                     |
| M        program             |
+------------------------------+
```

Память данных

```text
+------------------------------+
| 0        number_or_char      |
| 1        number_or_char      |
|      ...                     |
| M        number_or_char      |
+------------------------------+
```


---
## Инструкции процессора по умолчанию

| **Инструкции** | **Операция**           | **Формат**                  | **Описание**                                       |
|---------------------|------------------------|-----------------------------|----------------------------------------------------|
| **load**            | Загрузка значения      | `00001 Rdest, Число`        | Загружает число в регистр `Rdest`.                  |
| **load_from**      | Загрузка из адреса     | `00010 Rdest, Адрес`        | Загружает значение из указанного адреса в `Rdest`.  |
| **store**           | Сохранение в адрес     | `00011 Rsrc, Адрес`         | Сохраняет значение из `Rsrc` по указанному адресу.   |
| **store_to**        | Сохранение из адреса   | `01111 Rsrc, Адрес`         | Сохраняет значение из `Rsrc` в указанный адрес.      |
| **add**             | Сложение регистров     | `00100 Rdest, Rsrc`         | Выполняет сложение `Rdest = Rdest + Rsrc`.           |
| **sub**             | Вычитание регистров    | `00101 Rdest, Rsrc`         | Выполняет вычитание `Rdest = Rdest - Rsrc`.          |
| **cmp**             | Сравнение регистров    | `00110 Rsrc1, Rsrc2`        | Сравнивает значения регистров `Rsrc1` и `Rsrc2`.     |
| **jmp**             | Безусловный переход    | `00111 Адрес`                | Переходит по указанному адресу.                      |
| **je**              | Переход, если равно     | `01000 Адрес`                | Переходит по адресу, если результаты сравнения равны.|
| **jn**              | Переход, если отрицательно  | `01001 Адрес`                | Переходит по адресу, если результаты сравнения не равны.|
| **input**           | Ввод числа             | `01011 Rdest, Порт`          | Считывает число с порта ввода и сохраняет в `Rdest`. |
| **inputchar**       | Ввод символа           | `01100 Rdest, Порт`          | Считывает символ с порта ввода и сохраняет в `Rdest`.|
| **output**          | Вывод числа            | `01101 Rsrc, Порт`           | Выводит значение из `Rsrc` на порт вывода.           |
| **outputchar**      | Вывод символа          | `01110 Rsrc, Порт`           | Выводит символ из `Rsrc` на порт вывода.             |
| **mod**             | Остаток от деления     | `11111 Rdest, Rdest`      | Вычисляет остаток от деления `Rdest` на `Rdest`.   |
| **stop**            | Остановка программы    | `01111 000000000, 000000000`| Останавливает выполнение программы.                  |

### Формат инструкции (51 бит):

- **5 бит:** Опкод
- **23 бит:** Первый операнд (`Rdest` или другой регистр/параметр)
- **23 бит:** Второй операнд (`Rsrc`, число, адрес или порт)

### Микрокоманды и управляющие сигналы

Каждая микроинструкция состоит из последовательности микрокоманд, которые управляют выполнением операции. Ниже представлены основные микрокоманды и их функции:

| **Название сигнала** | **Тип**           | **Описание**                                                                 |
|----------------------|-------------------|-------------------------------------------------------------------------------|
| **load_enable**      | 1 бит   | Активирует загрузку числа в регистр назначения (`Rdest`).                    |
| **load_from_enable** | 1 бит  | Активирует загрузку значения из указанного адреса в регистр назначения (`Rdest`). |
| **store_enable**     | 1 бит   | Активирует сохранение значения из регистра источника (`Rsrc`) по указанному адресу. |
| **alu_enable**       | 1 бит   | Включает арифметико-логическое устройство (ALU) для выполнения операций `add`, `sub`, `mod`, `cmp`. |
| **alu_op**           | 2 бита | Определяет операцию, которую выполняет ALU (`add`, `sub`, `mod`, `cmp`).       |
| **read_enable**     | 1 бит    | Активирует сигнал чтения для операций ввода (`input`, `inputchar`).          |
| **write_enable**    | 1 бит    | Активирует сигнал записи для операций вывода (`output`, `outputchar`).        |
| **jump**            | 1 бит    | Активирует безусловный или условный переход по указанному адресу.             |
| **branch**          | 2 бита | Устанавливает условие перехода (`je`, `jn` и т.д.).                 |
| **halt**            | 1 бит    | Останавливает выполнение программы.                                           |
| **reg_src**         | 2 бита | Указывает регистр источника (`Rsrc`) для операций `store`, `add`, `sub`, `mod`, `cmp`, `output`, `outputchar`. |
| **reg_dest**        | 2 бита | Указывает регистр назначения (`Rdest`) для операций `load`, `add`, `sub`, `mod`, `input`, `inputchar`. |
| **immediate**       | 23 бита | Содержит непосредственное значение для операций `load`.                      |
| **address**         | 23 бита | Указывает адрес для операций `store`, `jmp`, `je`, `jne`, `isneg`.            |
| **port**            | 23 бита | Указывает порт для операций ввода (`input`, `inputchar`) и вывода (`output`, `outputchar`). |
| **input_type**      | 2 бита | Определяет тип ввода (`number` или `char`) для операций `input`, `inputchar`.  |
| **output_type**     | 2 бита | Определяет тип вывода (`number` или `char`) для операций `output`, `outputchar`. |

---

## Транслятор

---

## Control Unit

![Control Unit](./images/controlunit.png)

## DataPath

![DataPath](./images/datapath.png)

P.s. Под MUX, подрузамеваются и схемы типа MUX-DEMUX

---
## Тестирование

Тестирование выполняется при помощи golden test-ов
Алгоритмы:

* [cat](SwagLangPrograms/cat.sl)
* [hello](SwagLangPrograms/hello.sl)
* [helloUser](SwagLangPrograms/helloUser.sl)
* [prob2](SwagLangPrograms/prob2.sl)

Интеграционные тесты реализованы в модуле [golden_asm_test](./golden_asm_test.py) в виде golden тестов.

---

## Таблица проектов

| **ФИО**                      | **Проект**         | **LoC** | **Code байт** | **Инстр.** | **Такт.** | **Вариант**                                      |
|------------------------------|--------------------|---------|---------------|------------|-----------|--------------------------------------------------|
| Лукьянчук Ярослав Евгеньевич | Hello, Yaroslav!   | 90      | 701          | 402        | 2011       | asm, risc, harv, mc, instr, binary, stream, port, cstr, prob2 |
| Лукьянчук Ярослав Евгеньевич | Hello, world!      | 19      | 229          | 123         | 617       | asm, risc, harv, mc, instr, binary, stream, port, cstr, prob2 |
| Лукьянчук Ярослав Евгеньевич | Cat_some_cat       | 30      | 114           | 81         | 407       | asm, risc, harv, mc, instr, binary, stream, port, cstr, prob2 |
| Лукьянчук Ярослав Евгеньевич | Problem 2          | 87      | 420          | 603         | 3019       | asm, risc, harv, mc, instr, binary, stream, port, cstr, prob2 |
