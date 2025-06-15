//
// Generated file, do not edit! Created by opp_msgtool 6.0 from Volt.msg.
//

// Disable warnings about unused variables, empty switch stmts, etc:
#ifdef _MSC_VER
#  pragma warning(disable:4101)
#  pragma warning(disable:4065)
#endif

#if defined(__clang__)
#  pragma clang diagnostic ignored "-Wshadow"
#  pragma clang diagnostic ignored "-Wconversion"
#  pragma clang diagnostic ignored "-Wunused-parameter"
#  pragma clang diagnostic ignored "-Wc++98-compat"
#  pragma clang diagnostic ignored "-Wunreachable-code-break"
#  pragma clang diagnostic ignored "-Wold-style-cast"
#elif defined(__GNUC__)
#  pragma GCC diagnostic ignored "-Wshadow"
#  pragma GCC diagnostic ignored "-Wconversion"
#  pragma GCC diagnostic ignored "-Wunused-parameter"
#  pragma GCC diagnostic ignored "-Wold-style-cast"
#  pragma GCC diagnostic ignored "-Wsuggest-attribute=noreturn"
#  pragma GCC diagnostic ignored "-Wfloat-conversion"
#endif

#include <iostream>
#include <sstream>
#include <memory>
#include <type_traits>
#include "Volt_m.h"

namespace omnetpp {

// Template pack/unpack rules. They are declared *after* a1l type-specific pack functions for multiple reasons.
// They are in the omnetpp namespace, to allow them to be found by argument-dependent lookup via the cCommBuffer argument

// Packing/unpacking an std::vector
template<typename T, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::vector<T,A>& v)
{
    int n = v.size();
    doParsimPacking(buffer, n);
    for (int i = 0; i < n; i++)
        doParsimPacking(buffer, v[i]);
}

template<typename T, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::vector<T,A>& v)
{
    int n;
    doParsimUnpacking(buffer, n);
    v.resize(n);
    for (int i = 0; i < n; i++)
        doParsimUnpacking(buffer, v[i]);
}

// Packing/unpacking an std::list
template<typename T, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::list<T,A>& l)
{
    doParsimPacking(buffer, (int)l.size());
    for (typename std::list<T,A>::const_iterator it = l.begin(); it != l.end(); ++it)
        doParsimPacking(buffer, (T&)*it);
}

template<typename T, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::list<T,A>& l)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        l.push_back(T());
        doParsimUnpacking(buffer, l.back());
    }
}

// Packing/unpacking an std::set
template<typename T, typename Tr, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::set<T,Tr,A>& s)
{
    doParsimPacking(buffer, (int)s.size());
    for (typename std::set<T,Tr,A>::const_iterator it = s.begin(); it != s.end(); ++it)
        doParsimPacking(buffer, *it);
}

template<typename T, typename Tr, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::set<T,Tr,A>& s)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        T x;
        doParsimUnpacking(buffer, x);
        s.insert(x);
    }
}

// Packing/unpacking an std::map
template<typename K, typename V, typename Tr, typename A>
void doParsimPacking(omnetpp::cCommBuffer *buffer, const std::map<K,V,Tr,A>& m)
{
    doParsimPacking(buffer, (int)m.size());
    for (typename std::map<K,V,Tr,A>::const_iterator it = m.begin(); it != m.end(); ++it) {
        doParsimPacking(buffer, it->first);
        doParsimPacking(buffer, it->second);
    }
}

template<typename K, typename V, typename Tr, typename A>
void doParsimUnpacking(omnetpp::cCommBuffer *buffer, std::map<K,V,Tr,A>& m)
{
    int n;
    doParsimUnpacking(buffer, n);
    for (int i = 0; i < n; i++) {
        K k; V v;
        doParsimUnpacking(buffer, k);
        doParsimUnpacking(buffer, v);
        m[k] = v;
    }
}

// Default pack/unpack function for arrays
template<typename T>
void doParsimArrayPacking(omnetpp::cCommBuffer *b, const T *t, int n)
{
    for (int i = 0; i < n; i++)
        doParsimPacking(b, t[i]);
}

template<typename T>
void doParsimArrayUnpacking(omnetpp::cCommBuffer *b, T *t, int n)
{
    for (int i = 0; i < n; i++)
        doParsimUnpacking(b, t[i]);
}

// Default rule to prevent compiler from choosing base class' doParsimPacking() function
template<typename T>
void doParsimPacking(omnetpp::cCommBuffer *, const T& t)
{
    throw omnetpp::cRuntimeError("Parsim error: No doParsimPacking() function for type %s", omnetpp::opp_typename(typeid(t)));
}

template<typename T>
void doParsimUnpacking(omnetpp::cCommBuffer *, T& t)
{
    throw omnetpp::cRuntimeError("Parsim error: No doParsimUnpacking() function for type %s", omnetpp::opp_typename(typeid(t)));
}

}  // namespace omnetpp

Register_Class(Volt)

Volt::Volt(const char *name, short kind) : ::omnetpp::cPacket(name, kind)
{
}

Volt::Volt(const Volt& other) : ::omnetpp::cPacket(other)
{
    copy(other);
}

Volt::~Volt()
{
}

Volt& Volt::operator=(const Volt& other)
{
    if (this == &other) return *this;
    ::omnetpp::cPacket::operator=(other);
    copy(other);
    return *this;
}

void Volt::copy(const Volt& other)
{
    this->ackFlag = other.ackFlag;
    this->seqNumber = other.seqNumber;
    this->windowSize = other.windowSize;
}

void Volt::parsimPack(omnetpp::cCommBuffer *b) const
{
    ::omnetpp::cPacket::parsimPack(b);
    doParsimPacking(b,this->ackFlag);
    doParsimPacking(b,this->seqNumber);
    doParsimPacking(b,this->windowSize);
}

void Volt::parsimUnpack(omnetpp::cCommBuffer *b)
{
    ::omnetpp::cPacket::parsimUnpack(b);
    doParsimUnpacking(b,this->ackFlag);
    doParsimUnpacking(b,this->seqNumber);
    doParsimUnpacking(b,this->windowSize);
}

bool Volt::getFlags()
{
    return this->flags;
}

void Volt::setFlags(bool flags)
{
    this->flags = flags;
}

// 7 6 5 4 3 2 1 0 [Bit id]
// 0 0 0 0 0 0 0 0
// - - - - - - R A
// - - - - - - E C
// - - - - - - T K

#define ACK_FLAG (1 << 0) // 0 //00000001
#define RET_FLAG (1 << 1) // 1 //00000010

bool Volt::getAckFlag() {
    return getFlags() & ACK_FLAG;
}

void Volt::setAckFlag(bool ackFlag) {
    bool mask = ackFlag ? ACK_FLAG : 0;
    bool flags = getFlags();

    // Seteamos el ACK en 0
    // XXXXXXXX flags
    // 11111110 ~ACK_FLAG  (AND)
    // XXXXXXX0
    flags = flags & ~ACK_FLAG;

    // Si era true volvemos a poner esa flag
    flags = flags | mask;
    // Caso ackFlag = false
    // 00000000 mask
    // XXXXXXX0 getFlags OR
    // XXXXXXX0 resultado
    // Caso ackFlag = true
    // 00000001 mask
    // XXXXXXX0 getFlags OR
    // XXXXXXX1 resultado
    setFlags(flags);
}

bool Volt::getRetFlag() {
    return getFlags() & RET_FLAG;
}

void Volt::setRetFlag(bool retFlag) {
    bool mask = retFlag ? RET_FLAG : 0;
    bool flags = getFlags();

    // Seteamos el RET en 0
    // XXXXXXXX flags
    // 11111101 ~RET_FLAG  (AND)
    // XXXXXX0X
    flags = flags & ~RET_FLAG;

    // Si era true volvemos a poner esa flag
    flags = flags | mask;
    // Caso retFlag = false
    // 00000000 mask
    // XXXXXX0X getFlags OR
    // XXXXXX0x resultado
    // Caso retFlag = true
    // 00000010 mask
    // XXXXXX0X getFlags OR
    // XXXXXX1X resultado
    setFlags(flags);
}

int Volt::getSeqNumber() const
{
    return this->seqNumber;
}

void Volt::setSeqNumber(int seqNumber)
{
    this->seqNumber = seqNumber;
}

int Volt::getWindowSize() const
{
    return this->windowSize;
}

void Volt::setWindowSize(int windowSize)
{
    this->windowSize = windowSize;
}

class VoltDescriptor : public omnetpp::cClassDescriptor
{
  private:
    mutable const char **propertyNames;
    enum FieldConstants {
        FIELD_ackFlag,
        FIELD_seqNumber,
        FIELD_windowSize,
    };
  public:
    VoltDescriptor();
    virtual ~VoltDescriptor();

    virtual bool doesSupport(omnetpp::cObject *obj) const override;
    virtual const char **getPropertyNames() const override;
    virtual const char *getProperty(const char *propertyName) const override;
    virtual int getFieldCount() const override;
    virtual const char *getFieldName(int field) const override;
    virtual int findField(const char *fieldName) const override;
    virtual unsigned int getFieldTypeFlags(int field) const override;
    virtual const char *getFieldTypeString(int field) const override;
    virtual const char **getFieldPropertyNames(int field) const override;
    virtual const char *getFieldProperty(int field, const char *propertyName) const override;
    virtual int getFieldArraySize(omnetpp::any_ptr object, int field) const override;
    virtual void setFieldArraySize(omnetpp::any_ptr object, int field, int size) const override;

    virtual const char *getFieldDynamicTypeString(omnetpp::any_ptr object, int field, int i) const override;
    virtual std::string getFieldValueAsString(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldValueAsString(omnetpp::any_ptr object, int field, int i, const char *value) const override;
    virtual omnetpp::cValue getFieldValue(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldValue(omnetpp::any_ptr object, int field, int i, const omnetpp::cValue& value) const override;

    virtual const char *getFieldStructName(int field) const override;
    virtual omnetpp::any_ptr getFieldStructValuePointer(omnetpp::any_ptr object, int field, int i) const override;
    virtual void setFieldStructValuePointer(omnetpp::any_ptr object, int field, int i, omnetpp::any_ptr ptr) const override;
};

Register_ClassDescriptor(VoltDescriptor)

VoltDescriptor::VoltDescriptor() : omnetpp::cClassDescriptor(omnetpp::opp_typename(typeid(Volt)), "omnetpp::cPacket")
{
    propertyNames = nullptr;
}

VoltDescriptor::~VoltDescriptor()
{
    delete[] propertyNames;
}

bool VoltDescriptor::doesSupport(omnetpp::cObject *obj) const
{
    return dynamic_cast<Volt *>(obj)!=nullptr;
}

const char **VoltDescriptor::getPropertyNames() const
{
    if (!propertyNames) {
        static const char *names[] = {  nullptr };
        omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
        const char **baseNames = base ? base->getPropertyNames() : nullptr;
        propertyNames = mergeLists(baseNames, names);
    }
    return propertyNames;
}

const char *VoltDescriptor::getProperty(const char *propertyName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    return base ? base->getProperty(propertyName) : nullptr;
}

int VoltDescriptor::getFieldCount() const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    return base ? 3+base->getFieldCount() : 3;
}

unsigned int VoltDescriptor::getFieldTypeFlags(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldTypeFlags(field);
        field -= base->getFieldCount();
    }
    static unsigned int fieldTypeFlags[] = {
        FD_ISEDITABLE,    // FIELD_ackFlag
        FD_ISEDITABLE,    // FIELD_seqNumber
        FD_ISEDITABLE,    // FIELD_windowSize
    };
    return (field >= 0 && field < 3) ? fieldTypeFlags[field] : 0;
}

const char *VoltDescriptor::getFieldName(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldName(field);
        field -= base->getFieldCount();
    }
    static const char *fieldNames[] = {
        "ackFlag",
        "seqNumber",
        "windowSize",
    };
    return (field >= 0 && field < 3) ? fieldNames[field] : nullptr;
}

int VoltDescriptor::findField(const char *fieldName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    int baseIndex = base ? base->getFieldCount() : 0;
    if (strcmp(fieldName, "ackFlag") == 0) return baseIndex + 0;
    if (strcmp(fieldName, "seqNumber") == 0) return baseIndex + 1;
    if (strcmp(fieldName, "windowSize") == 0) return baseIndex + 2;
    return base ? base->findField(fieldName) : -1;
}

const char *VoltDescriptor::getFieldTypeString(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldTypeString(field);
        field -= base->getFieldCount();
    }
    static const char *fieldTypeStrings[] = {
        "bool",    // FIELD_ackFlag
        "int",    // FIELD_seqNumber
        "int",    // FIELD_windowSize
    };
    return (field >= 0 && field < 3) ? fieldTypeStrings[field] : nullptr;
}

const char **VoltDescriptor::getFieldPropertyNames(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldPropertyNames(field);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    }
}

const char *VoltDescriptor::getFieldProperty(int field, const char *propertyName) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldProperty(field, propertyName);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    }
}

int VoltDescriptor::getFieldArraySize(omnetpp::any_ptr object, int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldArraySize(object, field);
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        default: return 0;
    }
}

void VoltDescriptor::setFieldArraySize(omnetpp::any_ptr object, int field, int size) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldArraySize(object, field, size);
            return;
        }
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        default: throw omnetpp::cRuntimeError("Cannot set array size of field %d of class 'Volt'", field);
    }
}

const char *VoltDescriptor::getFieldDynamicTypeString(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldDynamicTypeString(object,field,i);
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        default: return nullptr;
    }
}

std::string VoltDescriptor::getFieldValueAsString(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldValueAsString(object,field,i);
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        case FIELD_ackFlag: return bool2string(pp->getAckFlag());
        case FIELD_seqNumber: return long2string(pp->getSeqNumber());
        case FIELD_windowSize: return long2string(pp->getWindowSize());
        default: return "";
    }
}

void VoltDescriptor::setFieldValueAsString(omnetpp::any_ptr object, int field, int i, const char *value) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldValueAsString(object, field, i, value);
            return;
        }
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        case FIELD_ackFlag: pp->setAckFlag(string2bool(value)); break;
        case FIELD_seqNumber: pp->setSeqNumber(string2long(value)); break;
        case FIELD_windowSize: pp->setWindowSize(string2long(value)); break;
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'Volt'", field);
    }
}

omnetpp::cValue VoltDescriptor::getFieldValue(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldValue(object,field,i);
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        case FIELD_ackFlag: return pp->getAckFlag();
        case FIELD_seqNumber: return pp->getSeqNumber();
        case FIELD_windowSize: return pp->getWindowSize();
        default: throw omnetpp::cRuntimeError("Cannot return field %d of class 'Volt' as cValue -- field index out of range?", field);
    }
}

void VoltDescriptor::setFieldValue(omnetpp::any_ptr object, int field, int i, const omnetpp::cValue& value) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldValue(object, field, i, value);
            return;
        }
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        case FIELD_ackFlag: pp->setAckFlag(value.boolValue()); break;
        case FIELD_seqNumber: pp->setSeqNumber(omnetpp::checked_int_cast<int>(value.intValue())); break;
        case FIELD_windowSize: pp->setWindowSize(omnetpp::checked_int_cast<int>(value.intValue())); break;
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'Volt'", field);
    }
}

const char *VoltDescriptor::getFieldStructName(int field) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldStructName(field);
        field -= base->getFieldCount();
    }
    switch (field) {
        default: return nullptr;
    };
}

omnetpp::any_ptr VoltDescriptor::getFieldStructValuePointer(omnetpp::any_ptr object, int field, int i) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount())
            return base->getFieldStructValuePointer(object, field, i);
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        default: return omnetpp::any_ptr(nullptr);
    }
}

void VoltDescriptor::setFieldStructValuePointer(omnetpp::any_ptr object, int field, int i, omnetpp::any_ptr ptr) const
{
    omnetpp::cClassDescriptor *base = getBaseClassDescriptor();
    if (base) {
        if (field < base->getFieldCount()){
            base->setFieldStructValuePointer(object, field, i, ptr);
            return;
        }
        field -= base->getFieldCount();
    }
    Volt *pp = omnetpp::fromAnyPtr<Volt>(object); (void)pp;
    switch (field) {
        default: throw omnetpp::cRuntimeError("Cannot set field %d of class 'Volt'", field);
    }
}

namespace omnetpp {

}  // namespace omnetpp

