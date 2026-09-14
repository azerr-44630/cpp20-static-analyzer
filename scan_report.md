# 🛡️ AST Təhlükəsizlik və Yaddaş Təhlili Hesabatı

- **Skan Tarixi:** `2026-09-14 10:23:01`
- **Aşkar Edilən Problem Sayı:** `7`

---

## 📊 Nəticələrin İcmal Cədvəli

| Dərəcə | Kateqoriya | Fayl | Halların Sayı |
|---|---|---|---|
| **HIGH** | Memory Leak | `./demo_vulnerable.cpp` | 1 |
| **MEDIUM** | Raw Pointer | `./demo_vulnerable.cpp` | 1 |
| **HIGH** | Rule of 5 | `./demo_vulnerable.cpp` | 1 |
| **HIGH** | Memory Leak | `./demo_vulnerable.cpp` | 1 |
| **MEDIUM** | Raw Pointer | `./demo_vulnerable.cpp` | 1 |
| **HIGH** | Rule of 5 | `./demo_vulnerable.cpp` | 1 |
| **MEDIUM** | Memory Management | `./demo_vulnerable.cpp` | 1 |

---

## 🔍 Detallı Xətalar və Tövsiyə Olunan Həllər

### 1. [HIGH] Memory Leak
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Polimorfik baza class-da destruktor virtual elan edilməyib.
- **Tövsiyə olunan həll:**
```cpp
public:
    virtual ~ClassName() = default;
```

### 2. [MEDIUM] Raw Pointer
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Dinamik yaddaş ayırmaq üçün raw pointer istifadə olunur.
- **Tövsiyə olunan həll:**
```cpp
std::unique_ptr və ya std::make_unique istifadə edin.
```

### 3. [HIGH] Rule of 5
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Dinamik resurs saxlayan sinifdə Rule of Five reallaşdırılmalıdır.
- **Tövsiyə olunan həll:**
```cpp
Copy Constructor və Assignment Operator-da Deep Copy yazılmalıdır.
```

### 4. [HIGH] Memory Leak
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Polimorfik baza class-da destruktor virtual elan edilməyib.
- **Tövsiyə olunan həll:**
```cpp
public:
    virtual ~ClassName() = default;
```

### 5. [MEDIUM] Raw Pointer
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Dinamik yaddaş ayırmaq üçün raw pointer istifadə olunur.
- **Tövsiyə olunan həll:**
```cpp
std::unique_ptr və ya std::make_unique istifadə edin.
```

### 6. [HIGH] Rule of 5
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Dinamik resurs saxlayan sinifdə Rule of Five reallaşdırılmalıdır.
- **Tövsiyə olunan həll:**
```cpp
Copy Constructor və Assignment Operator-da Deep Copy yazılmalıdır.
```

### 7. [MEDIUM] Memory Management
- **Fayl:** `./demo_vulnerable.cpp`
- **Aşkar olunma sayısı:** 1
- **Problem:** Manual delete istifadəsi RAII prinsiplərinə ziddir.
- **Tövsiyə olunan həll:**
```cpp
Resurs idarəsini Smart Pointer və ya konteynerlərə həvalə edin.
```
