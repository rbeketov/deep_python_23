#include <Python.h>
#include <ctype.h>


static void skip_space(const char** current) {
    while (**current && isspace((unsigned char)**current)) {
        (*current)++;
    }
}

static void skip_in_quotation_marks(const char** current) {
    while (**current && **current != '"') {
        (*current)++;
    }
}


static PyObject* parse_json(const char* json_str) {
    PyObject* parsed_dict = PyDict_New();
    if (parsed_dict == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to create a dictionary");
        return NULL;
    }

    const char* current = json_str;

    skip_space(&current);
    if (*current != '{') {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected an object");
        Py_DECREF(parsed_dict);
        return NULL;
    }
    current++;

    while (*current && *current != '}') {
        skip_space(&current);

        if (*current != '"') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected a string key");
            Py_DECREF(parsed_dict);
            return NULL;
        }
        current++;  // Пропускаем открывающую кавычку

        const char* key_start = current;

        skip_in_quotation_marks(&current);

        // Парсим ключ (ожидаем строку в двойных кавычках)
        if (*current != '"') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Unclosed string key");
            Py_DECREF(parsed_dict);
            return NULL;
        }

        PyObject* key = NULL;
        key = PyUnicode_DecodeUTF8(key_start, current - key_start, "strict");
        if (key == NULL) {
            Py_DECREF(parsed_dict);
            return NULL;
        }
        current++;  // Пропускаем закрывающую кавычку
        skip_space(&current);

        if (*current != ':') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected a colon after the key");
            Py_DECREF(key);
            Py_DECREF(parsed_dict);
            return NULL;
        }
        current++; // Пропускаем двоеточие

        skip_space(&current);

        PyObject* value = NULL;
        if (*current == '"') {
            // Строка
            current++;
            const char* value_start = current;

            skip_in_quotation_marks(&current);

            if (*current != '"') {
                PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Unclosed string value");
                Py_DECREF(key);
                Py_XDECREF(value);
                Py_DECREF(parsed_dict);
                return NULL;
            }

            value = PyUnicode_DecodeUTF8(value_start, current - value_start, "strict");
            current++;  // Пропускаем закрывающую кавычку
        } else if (isdigit((unsigned char)*current) || (*current == '-' && isdigit((unsigned char)*(current + 1)))) {
            // Число
            char* endptr;
            double num_value = strtod(current, &endptr);
            if (endptr == current) {
                PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected a number");
                Py_DECREF(key);
                Py_DECREF(parsed_dict);
                return NULL;
            }
            if (strchr(current, '.') && strchr(current, '.') < endptr) {
                value = Py_BuildValue("d", num_value);
            } else {
                value = Py_BuildValue("L", (long long)num_value);
            }
            current = endptr;
        } else {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected a string or number value");
            Py_DECREF(key);
            Py_DECREF(parsed_dict);
            return NULL;
        }

        if (PyDict_SetItem(parsed_dict, key, value) < 0) {
            PyErr_SetString(PyExc_RuntimeError, "Failed to set item in the dictionary");
            Py_DECREF(key);
            Py_DECREF(value);
            Py_DECREF(parsed_dict);
            return NULL;
        }

        Py_DECREF(key);
        Py_DECREF(value);

        skip_space(&current);

        if (*current == ',') {
            current++;
        } else if (*current != '}') {
            PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected a comma or closing brace");
            Py_DECREF(parsed_dict);
            return NULL;
        }
    }

    if (*current != '}') {
        PyErr_SetString(PyExc_ValueError, "Invalid JSON format: Expected a closing brace");
        Py_DECREF(parsed_dict);
        return NULL;
    }

    return parsed_dict;
}

static PyObject* cjson_loads(PyObject* self, PyObject* args) {
    const char* json_str;

    if (!PyArg_ParseTuple(args, "s", &json_str)) {
        PyErr_SetString(PyExc_TypeError, "Expected a string");
        return NULL;
    }

    PyObject* parsed_dict = parse_json(json_str);

    return parsed_dict;
}



static int write_key_value(PyObject *key, PyObject *value, char **output, Py_ssize_t *output_size);

static void append_str_to_output(const char *str, char **output, Py_ssize_t *output_size) {
    if (!str || !output_size) {
        PyErr_SetString(PyExc_RuntimeError, "Error in str_to_output, inputed NULL");
        return;
    }
    Py_ssize_t len = strlen(str);
    *output_size += len;
    if (output) {
        memcpy(*output, str, len);
        *output += len;
    }
}

static void append_char_to_output(char c, char **output, Py_ssize_t *output_size) {
    if (!output_size) {
        PyErr_SetString(PyExc_RuntimeError, "Error in char_to_output, inputed NULL");
        return;
    }
    (*output_size)++;
    if (output) {
        *(*output)++ = c;
    }
}

static void append_json_string(PyObject *str_obj, char **output, Py_ssize_t *output_size) {
    PyObject *unicode = PyUnicode_AsUTF8String(str_obj);
    const char *utf8_str = PyBytes_AsString(unicode);
    append_char_to_output('"', output, output_size);
    append_str_to_output(utf8_str, output, output_size);
    append_char_to_output('"', output, output_size);

    Py_DECREF(unicode);
}

static void append_json_number(PyObject *num_obj, char **output, Py_ssize_t *output_size) {
    PyObject *num_str_obj = PyObject_Str(num_obj);
    const char *num_str = PyUnicode_AsUTF8(num_str_obj);
    append_str_to_output(num_str, output, output_size);

    Py_DECREF(num_str_obj);
}


static int write_key_value(PyObject *key, PyObject *value, char **output, Py_ssize_t *output_size) {
    if (key == NULL || value == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "Key or value is missing");
        return -1;
    }

    if (!PyUnicode_Check(key)) {
        PyErr_SetString(PyExc_TypeError, "Key must be a string");
        return -1;
    }

    if (PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "Nested dictionaries are not supported");
        return -1;
    }

    append_json_string(key, output, output_size);
    append_char_to_output(':', output, output_size);
    append_char_to_output(' ', output, output_size);

    if (PyUnicode_Check(value)) {
        append_json_string(value, output, output_size);
    } else if (PyLong_Check(value) || PyFloat_Check(value)) {
        append_json_number(value, output, output_size);
    } else {
        PyErr_SetString(PyExc_TypeError, "Unsupported value type");
        return -1;
    }

    return 0;
}

static PyObject* cjson_dumps(PyObject* self, PyObject* args) {

    PyObject* dict = NULL;
    if (!PyArg_ParseTuple(args, "O", &dict)) {
        PyErr_SetString(PyExc_TypeError, "Expected a dictionary");
        return NULL;
    }

    if (!PyDict_Check(dict)) {
        PyErr_SetString(PyExc_TypeError, "Argument must be a dictionary");
        return NULL;
    }

    Py_ssize_t output_size = 0;
    char *output = NULL;
    PyObject *key = NULL; 
    PyObject *value = NULL;

    Py_ssize_t pos = 0;
    while (PyDict_Next(dict, &pos, &key, &value)) {
        write_key_value(key, value, NULL, &output_size);

        if (pos < PyDict_Size(dict)) {
            output_size += 2; // для ", "
        }
    }
    output_size += 2;   // для {}

    output = (char *)malloc(output_size + 1);
    if (output == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate memory");
        return NULL;
    }

    pos = 0;
    output_size = 0;
    char *current_output = output;

    append_char_to_output('{', &current_output, &output_size);
    while (PyDict_Next(dict, &pos, &key, &value)) {
        write_key_value(key, value, &current_output, &output_size);
        if (pos < PyDict_Size(dict)) {
            append_char_to_output(',', &current_output, &output_size);
            append_char_to_output(' ', &current_output, &output_size);
        }
    }
    append_char_to_output('}', &current_output, &output_size);
    *current_output = '\0';

    PyObject *result = PyUnicode_DecodeUTF8(output, output_size, "strict");
    free(output);

    return result;
}


static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Load JSON string and return a Python dictionary"},
    {"dumps", cjson_dumps, METH_VARARGS, "Dump Python dictionary to a JSON string"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef cjson_module = {
    PyModuleDef_HEAD_INIT, "cjson", NULL, -1, methods
};


PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson_module);
}
