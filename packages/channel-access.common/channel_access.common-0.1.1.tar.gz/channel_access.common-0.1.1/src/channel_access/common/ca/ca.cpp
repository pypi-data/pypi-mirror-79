#include <initializer_list>

#include <Python.h>

#include <cadef.h>
#include <db_access.h>
#define epicsAlarmGLOBAL
#include <alarm.h>
#undef epicsAlarmGLOBAL



namespace ca {
namespace {

struct Entry {
    char const* text;
    long value;
};


PyDoc_STRVAR(status__doc__, R"(
Alarm status of a channel access PV.
)");
struct Status {
    static constexpr const char* name = "Status";
    static constexpr const char* doc = status__doc__;

    static int count() { return ALARM_NSTATUS; }
    static char const* text(int i) { return epicsAlarmConditionStrings[i]; };
    static long value(int i) { return i; }
};

PyDoc_STRVAR(severity__doc__, R"(
Alarm severity of a channel access PV.
)");
struct Severity {
    static constexpr const char* name = "Severity";
    static constexpr const char* doc = severity__doc__;

    static int count() { return ALARM_NSEV; }
    static char const* text(int i) { return epicsAlarmSeverityStrings[i]; };
    static long value(int i) { return i; }
};

PyDoc_STRVAR(field_type__doc__, R"(
Possible types of a channel access PV.
)");
struct Type {
    static constexpr const char* name = "Type";
    static constexpr const char* doc = field_type__doc__;

    static int count() { return dbf_text_dim - 2; }
    static char const* text(int i) { return dbf_type_to_text(i) + 4; };
    static long value(int i) { return i; }
};

PyDoc_STRVAR(access_rights__doc__, R"(
Access rights for channel access PVs.

These can be combined by or-ing them together.
)");
struct AccessRights {
    static constexpr auto entries = {
        Entry{"NO_ACCESS",    0},
        Entry{"READ_ACCESS",  1},
        Entry{"WRITE_ACCESS", 2},
        Entry{"RW_ACCESS",    3}
    };

    static constexpr const char* name = "AccessRights";
    static constexpr const char* doc = access_rights__doc__;

    static int count() { return entries.size(); }
    static char const* text(int i) { return entries.begin()[i].text; };
    static long value(int i) { return entries.begin()[i].value; }
};

PyDoc_STRVAR(trigger__doc__, R"(
Available event sources for channel access PVs.

These can be combined by or-ing them together.
)");
struct Events {
    static constexpr auto entries = {
        Entry{"NONE",     0},
        Entry{"VALUE",    DBE_VALUE},
        Entry{"ARCHIVE",  DBE_ARCHIVE},
        Entry{"ALARM",    DBE_ALARM},
        Entry{"PROPERTY", DBE_PROPERTY},
        Entry{"ALL",      DBE_VALUE | DBE_ARCHIVE | DBE_ALARM | DBE_PROPERTY}
    };

    static constexpr const char* name = "Events";
    static constexpr const char* doc = trigger__doc__;

    static int count() { return entries.size(); }
    static char const* text(int i) { return entries.begin()[i].text; };
    static long value(int i) { return entries.begin()[i].value; }
};

/* Add an enum or flag type to a module.
 *
 * EnumDef contains all the information to create the type.
 * type_class must be a callable creating the new type.
 */
template <typename EnumDef>
bool add_enum(PyObject* module)
{
    int const count = EnumDef::count();

    PyObject* list = PyList_New(count);
    if (not list) return false;

    for (int i = 0; i < count; ++i) {
        PyObject* entry = Py_BuildValue("(si)", EnumDef::text(i), EnumDef::value(i));
        if (not entry) {
            Py_DECREF(list);
            return false;
        }

        PyList_SET_ITEM(list, i, entry);
    }

    PyObject* obj = Py_BuildValue("(ssN)", EnumDef::name, EnumDef::doc, list);
    if (not obj) return false;

    if (PyModule_AddObject(module, EnumDef::name, obj) != 0) {
        PyErr_Format(PyExc_RuntimeError, "Could not add enum data for %s", EnumDef::name);
        return false;
    }

    return true;
}

PyDoc_STRVAR(ca__doc__, R"(
Low level wrapper module over the libca enums, flags and constants.

All values are taken directly from the header files.
)");
PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "channel_access.common.ca", /* name of module */
    ca__doc__,                  /* module documentation, may be NULL */
    -1,                         /* size of per-interpreter state of the module,
                                   or -1 if the module keeps state in global variables. */
};

} // namespace
} // namespace ca

extern "C" {

PyMODINIT_FUNC PyInit_ca(void)
{
    PyObject* module = PyModule_Create(&ca::module);
    if (not module) goto error;

    if (PyModule_AddIntConstant(module, "EPICS_EPOCH", POSIX_TIME_AT_EPICS_EPOCH) != 0) goto error;

    if (not ca::add_enum<ca::Severity>(module)) goto error;
    if (not ca::add_enum<ca::Status>(module)) goto error;
    if (not ca::add_enum<ca::Type>(module)) goto error;
    if (not ca::add_enum<ca::AccessRights>(module)) goto error;
    if (not ca::add_enum<ca::Events>(module)) goto error;

    return module;

error:
    Py_XDECREF(module);
    return nullptr;
}

}
