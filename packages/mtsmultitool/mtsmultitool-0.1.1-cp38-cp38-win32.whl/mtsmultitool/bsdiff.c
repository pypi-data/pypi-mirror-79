/*
 * This code is a combination of the Python bsdiff4 library (derived from
 * cx_bsdiff and bsdiff) and ARM Mbed's mbed-edge.  Binary diff algorithm
 * originates from bsdiff utility.  Python adaptation from bsdiff4.  Block
 * sizing with LZ4 compression from mbed-edge.
 *
 * bsdiff4 (https://github.com/ilanschnell/bsdiff4)
 * Copyright 2011-2019, Ilan Schnell
 *
 * cx_bsdiff (http://cx-bsdiff.sourceforge.net/)
 * Copyright 2002, Anthony Tuininga 
 *
 * http://www.daemonology.net/bsdiff/
 *
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

#include "lz4.h"


#define MIN(x, y)  (((x) < (y)) ? (x) : (y))


static void split(off_t *I, off_t *V, off_t start, off_t len, off_t h)
{
    off_t i, j, k, x, tmp, jj, kk;

    if (len < 16) {
        for (k = start; k < start + len; k += j) {
            j = 1;
            x = V[I[k] + h];
            for (i = 1; k + i < start + len; i++) {
                if (V[I[k + i] + h] < x) {
                    x = V[I[k + i] + h];
                    j = 0;
                }
                if (V[I[k + i] + h] == x) {
                    tmp = I[k + j];
                    I[k + j] = I[k + i];
                    I[k + i] = tmp;
                    j++;
                }
            }
            for (i = 0; i < j; i++)
                V[I[k + i]] = k + j - 1;
            if (j == 1)
                I[k] = -1;
        }

    } else {

        jj = 0;
        kk = 0;
        x = V[I[start + len / 2] + h];
        for (i = start; i < start + len; i++) {
            if (V[I[i] + h] < x)
                jj++;
            if (V[I[i] + h] == x)
                kk++;
        }
        jj += start;
        kk += jj;

        j = 0;
        k = 0;
        i = start;
        while (i < jj) {
            if (V[I[i] + h] < x) {
                i++;
            } else if (V[I[i] + h] == x) {
                tmp = I[i];
                I[i] = I[jj + j];
                I[jj + j] = tmp;
                j++;
            } else {
                tmp = I[i];
                I[i] = I[kk + k];
                I[kk + k] = tmp;
                k++;
            }
        }

        while (jj + j < kk) {
            if (V[I[jj + j] + h] == x) {
                j++;
            } else {
                tmp = I[jj + j];
                I[jj + j] = I[kk + k];
                I[kk + k] = tmp;
                k++;
            }
        }

        if (jj > start)
            split(I, V, start, jj - start, h);

        for (i = 0; i < kk - jj; i++)
            V[I[jj + i]] = kk - 1;
        if (jj == kk - 1)
            I[jj] = -1;
        if (start + len > kk)
            split(I, V, kk, start + len - kk, h);
    }
}


static void qsufsort(off_t *I, off_t *V, unsigned char *old, off_t oldsize)
{
    off_t buckets[256], i, h, len;

    for (i = 0; i < 256; i++)
        buckets[i] = 0;
    for (i = 0; i < oldsize; i++)
        buckets[old[i]]++;
    for (i = 1; i < 256; i++)
        buckets[i] += buckets[i - 1];
    for (i = 255; i > 0; i--)
        buckets[i] = buckets[i - 1];
    buckets[0] = 0;

    for (i = 0; i < oldsize; i++)
        I[++buckets[old[i]]] = i;
    I[0] = oldsize;
    for (i = 0; i < oldsize; i++)
        V[i] = buckets[old[i]];
    V[oldsize] = 0;
    for (i = 1; i < 256; i++)
        if (buckets[i] == buckets[i - 1] + 1)
            I[buckets[i]] = -1;
    I[0] = -1;

    for (h = 1; I[0] != -(oldsize + 1); h += h) {
        len = 0;
        for (i = 0; i < oldsize + 1;) {
            if (I[i] < 0) {
                len -= I[i];
                i -= I[i];
            } else {
                if (len)
                    I[i - len] = -len;
                len = V[I[i]] + 1 - i;
                split(I, V, i, len, h);
                i += len;
                len=0;
            }
        }
        if (len)
            I[i - len] = -len;
    }

    for (i = 0; i < oldsize + 1; i++)
        I[V[i]] = i;
}


static off_t matchlen(unsigned char *old, off_t oldsize,
                      unsigned char *new, off_t newsize)
{
    off_t i;

    for (i = 0; (i < oldsize) && (i < newsize); i++)
        if (old[i] != new[i])
            break;
    return i;
}


static off_t search(off_t *I,
                    unsigned char *old, off_t oldsize,
                    unsigned char *new, off_t newsize,
                    off_t st, off_t en, off_t *pos)
{
    off_t x, y;

    if (en - st < 2) {
        x = matchlen(old + I[st], oldsize - I[st], new, newsize);
        y = matchlen(old + I[en], oldsize - I[en], new, newsize);

        if (x > y) {
            *pos = I[st];
            return x;
        } else {
            *pos = I[en];
            return y;
        }
    }

    x = st + (en - st) / 2;
    if (memcmp(old + I[x], new, MIN(oldsize - I[x], newsize)) < 0) {
        return search(I, old, oldsize, new, newsize, x, en, pos);
    } else {
        return search(I, old, oldsize, new, newsize, st, x, pos);
    }
}

static void offtout(int64_t x, uint8_t *buf)
{
    int64_t y;

    if (x < 0)
        y = -x;
    else
        y = x;

    buf[0] = y % 256;
    y -= buf[0];
    y = y / 256;
    buf[1] = y % 256;
    y -= buf[1];
    y = y / 256;
    buf[2] = y % 256;
    y -= buf[2];
    y = y / 256;
    buf[3] = y % 256;
    y -= buf[3];
    y = y / 256;
    buf[4] = y % 256;
    y -= buf[4];
    y = y / 256;
    buf[5] = y % 256;
    y -= buf[5];
    y = y / 256;
    buf[6] = y % 256;
    y -= buf[6];
    y = y / 256;
    buf[7] = y % 256;

    if (x < 0)
        buf[7] |= 0x80;
}


/* >> 
 * varint.c from https://github.com/ARMmbed/mbed-edge
 *
 * Copyright (c) 2018-2019 ARM Limited
 * All rights reserved
*/

static const unsigned char VARINT_TOP_BIT_ON_BYTE = (128);
static const unsigned char VARINT_TOP_BIT_OFF_BYTE = (127);
static const int32_t VARINT_ERR_BUFFER_TOO_SMALL = -7;

static int encode_unsigned_varint(uint64_t value, unsigned char *buf, uint32_t BUFF_SIZE_MAX)
{
    unsigned int pos = 0;
    do {
        if (pos >= BUFF_SIZE_MAX) {
            return VARINT_ERR_BUFFER_TOO_SMALL;  // protecting buf from overwrite
        }
        buf[pos] = (char) value;
        value >>= 7;
        if (value > 0) {
            buf[pos] |= VARINT_TOP_BIT_ON_BYTE;
        } else {
            buf[pos] &= VARINT_TOP_BIT_OFF_BYTE;
        }
        pos++;
    } while (value > 0);

    return pos;
}

static int encode_signed_varint(int64_t value, unsigned char *buf, uint32_t BUFF_SIZE_MAX)
{
    unsigned int pos = 0;

    if (value < 0) {
        value = value * -1;  // change value to positive number.
        value <<= 1;
        value |= 1; // set lowest bit 1 if it was negative;
    } else {
        value <<= 1; // lower bit set to 0 if not negative.
    }

    do {
        if (pos >= BUFF_SIZE_MAX) {
            return VARINT_ERR_BUFFER_TOO_SMALL;  // protecting buf from overwrite
        }
        buf[pos] = (char) value;
        value >>= 7;
        if (value > 0) {
            buf[pos] |= VARINT_TOP_BIT_ON_BYTE;
        } else {
            buf[pos] &= VARINT_TOP_BIT_OFF_BYTE;
        }
        pos++;
    } while (value > 0);

    return pos;
}

/* << */


/* >> 
 * MultiTech 
 */

#define CONTROL_OFFSET  (16)
#define CONTROL_LEN     (24)

static int writeHeader(unsigned char * comp, int64_t newsize, const char* sig, const int64_t max_frame_size)
{
    memset(comp, 0, CONTROL_OFFSET);
    memcpy(comp, sig, strlen(sig));
    memset(&comp[CONTROL_OFFSET], 0, 24);
    offtout(newsize, &comp[CONTROL_OFFSET]);
    offtout(max_frame_size, &comp[CONTROL_OFFSET + 8]);

    return CONTROL_OFFSET + CONTROL_LEN;
}

static void updateHeader(unsigned char * comp, int64_t max_deCompressBuffer_size)
{
    offtout(max_deCompressBuffer_size, &comp[CONTROL_OFFSET + 16]);
}

/* << */

/* >>
 * Adapted from bsdiff.c (https://github.com/ARMmbed/mbed-edge)
 *
 * Copyright 2003-2005 Colin Percival
 * Copyright 2012 Matthew Endsley
 * Copyright (c) 2018-2019 ARM Limited
 * All rights reserved
 *
 * Modified by Taylor Heck for MultiTech
 *  - Write data to a buffer instead of a stream.
 *  - Use PyMem_Malloc and PyMem_Free
 */

static int writedeCompressBuffer(unsigned char * comp, const void* buffer, size_t length,
        size_t* max_deCompressBuffer_size, size_t max_frame_size, int* compressedSize)
{
    int src_ptr;
    char* temp;
    size_t deCompressBuffer_size;
    size_t written = 0;
    uint8_t buf[8];
    *compressedSize = 0;

    if (length == 0)
        return 0;

    temp = PyMem_Malloc(max_frame_size);
    src_ptr = MIN(length, max_frame_size);
    do {
        deCompressBuffer_size = LZ4_compress_destSize(buffer, temp, &src_ptr, max_frame_size);

        if (deCompressBuffer_size == 0) {
            PyMem_Free(temp);
            return -1;
        }

        int encodedSize = encode_unsigned_varint(deCompressBuffer_size, buf, sizeof(buf));

        if (encodedSize <= 0) {
            return encodedSize;  // error in encoding
        }

        memcpy(&comp[*compressedSize], buf, encodedSize);
        *compressedSize += encodedSize;

        memcpy(&comp[*compressedSize], temp, deCompressBuffer_size);
        *compressedSize += deCompressBuffer_size;

        buffer = (char*) buffer + src_ptr;
        written += src_ptr;

        src_ptr = MIN(length - written, max_frame_size);

        if (deCompressBuffer_size > *max_deCompressBuffer_size){
            *max_deCompressBuffer_size = deCompressBuffer_size;
        }


    } while (written != length);

    PyMem_Free(temp);
    return 0;
}
/* << */

/* performs a diff between the two data streams and returns a tuple
   containing the control, diff and extra blocks that bsdiff produces
*/
static PyObject* diff(PyObject* self, PyObject* args)
{
    // setvbuf (stdout, NULL, _IONBF, 0);
    off_t lastscan, lastpos, lastoffset, oldscore, scsc, overlap, Ss, lens;
    off_t *I, *V, complen, scan, pos, len, s, Sf, lenf, Sb, lenb, i;
    size_t max_deCompressBuffer_size;
    PyObject *temp;
    Py_ssize_t origDataLength, newDataLength;
    char *origData, *newData;
    unsigned char *db, *eb, *comp;
    Py_ssize_t maxFrameSize;
    const char* sig;

    if (!PyArg_ParseTuple(args, "y#y#ns",
                          &origData, &origDataLength,
                          &newData, &newDataLength,
                          &maxFrameSize, &sig)) {
        return NULL;
    }

    max_deCompressBuffer_size = 0;
    /* perform sort on original data */
    I = PyMem_Malloc((origDataLength + 1) * sizeof(off_t));
    if (!I) {
        return PyErr_NoMemory();
    }
    V = PyMem_Malloc((origDataLength + 1) * sizeof(off_t));
    if (!V) {
        PyMem_Free(I);
        return PyErr_NoMemory();
    }
    Py_BEGIN_ALLOW_THREADS  /* release GIL */
    qsufsort(I, V, (unsigned char *) origData, origDataLength);
    Py_END_ALLOW_THREADS
    PyMem_Free(V);

    /* allocate memory for the diff and extra blocks */
    db = PyMem_Malloc(newDataLength + 1);
    if (!db) {
        PyMem_Free(I);
        return PyErr_NoMemory();
    }

    /* Allocate buffer to store compressed diff */
    comp = PyMem_Malloc(newDataLength + 1 + CONTROL_OFFSET + CONTROL_LEN);
    if (!comp) {
        PyMem_Free(I);
        PyMem_Free(db);
        return PyErr_NoMemory();
    }

    eb = PyMem_Malloc(newDataLength + 1);
    if (!eb) {
        PyMem_Free(I);
        PyMem_Free(db);
        PyMem_Free(comp);
        return PyErr_NoMemory();
    }

    /* perform the diff */
    len = 0;
    scan = 0;
    lastscan = 0;
    lastpos = 0;
    lastoffset = 0;
    pos = 0;

    complen = writeHeader(comp, newDataLength, sig, maxFrameSize);
    
    while (scan < newDataLength) {
        oldscore = 0;

        Py_BEGIN_ALLOW_THREADS  /* release GIL */
        for (scsc = scan += len; scan < newDataLength; scan++) {
            len = search(I, (unsigned char *) origData, origDataLength,
                         (unsigned char *) newData + scan,
                         newDataLength - scan, 0, origDataLength, &pos);
            for (; scsc < scan + len; scsc++)
                if ((scsc + lastoffset < origDataLength) &&
                          (origData[scsc + lastoffset] == newData[scsc]))
                    oldscore++;
            if (((len == oldscore) && (len != 0)) || (len > oldscore + 8))
                break;
            if ((scan + lastoffset < origDataLength) &&
                      (origData[scan + lastoffset] == newData[scan]))
                oldscore--;
        }
        Py_END_ALLOW_THREADS

        if ((len != oldscore) || (scan == newDataLength)) {
            s = 0;
            Sf = 0;
            lenf = 0;
            for (i = 0; (lastscan + i < scan) &&
                     (lastpos + i < origDataLength);) {
                if (origData[lastpos + i] == newData[lastscan + i])
                    s++;
                i++;
                if (s * 2 - i > Sf * 2 - lenf) {
                    Sf = s;
                    lenf = i;
                }
            }

            lenb = 0;
            if (scan < newDataLength) {
                s = 0;
                Sb = 0;
                for (i = 1; (scan >= lastscan + i) && (pos >= i); i++) {
                    if (origData[pos - i] == newData[scan - i])
                        s++;
                    if (s * 2 - i > Sb * 2 - lenb) {
                        Sb = s;
                        lenb = i;
                    }
                }
            }

            if (lastscan + lenf > scan - lenb) {
                overlap = (lastscan + lenf) - (scan - lenb);
                s = 0;
                Ss = 0;
                lens = 0;
                for (i = 0; i < overlap; i++) {
                    if (newData[lastscan + lenf - overlap + i] ==
                            origData[lastpos + lenf - overlap + i])
                        s++;
                    if (newData[scan - lenb + i]== origData[pos - lenb + i])
                        s--;
                    if (s > Ss) {
                        Ss = s;
                        lens = i + 1;
                    }
                }

                lenf += lens - overlap;
                lenb -= lens;
            }

            /* >> Adapted from mbed-edge */
            int64_t diff_str_len = lenf;
            int64_t extra_str_len_y = (scan - lenb) - (lastscan + lenf);
            int64_t old_file_ctrl_off_set_jump = (pos - lenb) - (lastpos + lenf);

            /* Write control data */

            int encodedSize = encode_unsigned_varint(diff_str_len, &comp[complen], 8);

            assert(encodedSize > 0 && encodedSize <= 8);
            complen += encodedSize;

            encodedSize = encode_unsigned_varint(extra_str_len_y, &comp[complen], 8);
            assert(encodedSize > 0 && encodedSize <= 8);
            complen += encodedSize;

            encodedSize = encode_signed_varint(old_file_ctrl_off_set_jump, &comp[complen], 8);
            assert(encodedSize > 0 && encodedSize <= 8);
            complen += encodedSize;

            /* Write diff data */
            for (i = 0; i < lenf; i++) {
                db[i] = newData[lastscan + i] - origData[lastpos + i];
            }
            if (writedeCompressBuffer(&comp[complen], db, (size_t)diff_str_len, &max_deCompressBuffer_size, maxFrameSize, &encodedSize)) {
                PyMem_Free(db);
                PyMem_Free(eb);
                PyMem_Free(comp);
                return NULL;
            }
            complen += encodedSize;

            /* Write extra data */
            for (i = 0; i < extra_str_len_y; i++) {
                eb[i] = newData[lastscan + lenf + i];
            }
            if (writedeCompressBuffer(&comp[complen], eb, (size_t)extra_str_len_y, &max_deCompressBuffer_size, maxFrameSize, &encodedSize)) {
                PyMem_Free(db);
                PyMem_Free(eb);
                PyMem_Free(comp);
                return NULL;
            }
            complen += encodedSize;
            /* << */

            lastscan = scan - lenb;
            lastpos = pos - lenb;
            lastoffset = pos - scan;
        }
    }
    updateHeader(comp, max_deCompressBuffer_size);
    PyMem_Free(I);

    temp = PyBytes_FromStringAndSize((char *) comp, complen);
    PyMem_Free(db);
    PyMem_Free(eb);
    PyMem_Free(comp);

    
    return temp;
}


/* >>
 * Copyright 2020 MultiTech
 */
static PyObject* compress(PyObject* self, PyObject* args)
{
    setvbuf (stdout, NULL, _IONBF, 0);
    off_t complen;
    size_t max_deCompressBuffer_size;
    PyObject* temp;
    Py_ssize_t dataLength;
    char* data;
    unsigned char *comp, *cmpBuf;
    Py_ssize_t maxFrameSize;
    LZ4_stream_t* lz4Stream;
    const char* sig;

    if (!PyArg_ParseTuple(args, "y#ns",
                          &data, &dataLength,
                          &maxFrameSize, &sig)) {
        return NULL;
    }

    unsigned char* inpBuf[2];
    int  inpBufIndex = 0;

    inpBuf[0] = PyMem_Malloc(maxFrameSize);
    if (!inpBuf[0]) {
        return PyErr_NoMemory();
    }

    inpBuf[1] = PyMem_Malloc(maxFrameSize);
    if (!inpBuf[1]) {
        PyMem_Free(inpBuf[0]);
        return PyErr_NoMemory();
    }
    // Small files do not compress well and may end up larger than the original
    comp = PyMem_Malloc(dataLength + ((dataLength / maxFrameSize + 2) * 8));
    if (!comp) {
        PyMem_Free(inpBuf[0]);
        PyMem_Free(inpBuf[1]);
        return PyErr_NoMemory();
    }
    
    const size_t cmpBufSize = LZ4_COMPRESSBOUND(maxFrameSize);
    cmpBuf = PyMem_Malloc(cmpBufSize);
    if (!cmpBuf) {
        PyMem_Free(inpBuf[0]);
        PyMem_Free(inpBuf[1]);
        PyMem_Free(comp);
        return PyErr_NoMemory();
    }

    lz4Stream = LZ4_createStream();

    size_t read = 0;
    size_t read_size = maxFrameSize;
    size_t remaining = dataLength;
    char intBuf[4];

    memset(comp, 0, CONTROL_OFFSET);
    memcpy(comp, sig, strlen(sig));
    complen = CONTROL_OFFSET;

    for(;;) {
        unsigned char* const inpPtr = inpBuf[inpBufIndex];
        if (remaining < read_size) {
            read_size = remaining;
        }
        if (0 == read_size) {
            break;
        }
        memcpy(inpPtr, &data[read], read_size);

        {
            const int cmpBytes = LZ4_compress_fast_continue(
                lz4Stream, inpPtr, cmpBuf, read_size, cmpBufSize, 1);

            if (cmpBytes <= 0) {
                break;
            }

            intBuf[0] = (cmpBytes >> 24) & 0xFF;
            intBuf[1] = (cmpBytes >> 16) & 0xFF;
            intBuf[2] = (cmpBytes >>  8) & 0xFF;
            intBuf[3] = (cmpBytes >>  0) & 0xFF;
            memcpy(&comp[complen], intBuf, sizeof(intBuf));
            complen += sizeof(intBuf);
            memcpy(&comp[complen], cmpBuf, (size_t)cmpBytes);
            complen += cmpBytes;
        }

        inpBufIndex = (inpBufIndex + 1) % 2;
        remaining -= read_size;
        read += read_size;
    }

    memset(intBuf, 0, sizeof(intBuf));
    memcpy(&comp[complen], intBuf, sizeof(intBuf));
    complen += sizeof(intBuf);

    temp = PyBytes_FromStringAndSize((char *) comp, complen);
    PyMem_Free(inpBuf[0]);
    PyMem_Free(inpBuf[1]);
    PyMem_Free(comp);
    PyMem_Free(cmpBuf);

    return temp;
}

/* << */

/* declaration of methods supported by this module */
static PyMethodDef module_functions[] = {
    {"diff", diff, METH_VARARGS},
    {"compress", compress, METH_VARARGS},
    {NULL, NULL, 0, NULL}  /* Sentinel */
};

/* initialization routine for the shared libary */
#ifdef IS_PY3K
static PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "bsdiff", 0, -1, module_functions,
};

PyMODINIT_FUNC
PyInit_bsdiff(void)
{
    PyObject *m;

    m = PyModule_Create(&moduledef);
    if (m == NULL)
        return NULL;
    return m;
}
#else
PyMODINIT_FUNC
initbsdiff(void)
{
    Py_InitModule("bsdiff", module_functions);
}
#endif
