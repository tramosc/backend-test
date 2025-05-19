# 🚀 Com Build API

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-blue.svg)](https://fastapi.tiangolo.com/)

---

## 📋 Descripción general

**Com Build API** es un servicio backend robusto construido con **FastAPI** siguiendo una **Arquitectura Hexagonal** (también conocida como Puertos y Adaptadores).  
Este enfoque separa limpiamente la lógica de dominio de las preocupaciones externas, resultando en un código altamente mantenible, testeable e independiente del framework.

La aplicación está organizada en módulos (por ejemplo, usuarios, autenticación) con límites claros entre:

- la lógica de dominio
- los servicios de aplicación
- y los componentes de infraestructura.

---

## 🏗️ Arquitectura

El proyecto sigue una arquitectura estructurada por capas:

### 🔹 Capa de Dominio

- **Propósito**: Define las entidades de negocio centrales y la lógica de validación.
- **Ubicación**: `app/modules/users/domain/` (ej., `area.py`, `role.py`, `user.py`, `widget.py`)
- **Contiene**: Entidades, objetos de valor y modelos Pydantic para validación.

### 🔹 Capa de Aplicación

- **Propósito**: Orquesta la lógica de negocio y los casos de uso.
- **Ubicación**: `app/modules/users/application/` (ej., `user_service.py`, `widget_service.py`)
- **Contiene**: Servicios con reglas de negocio que coordinan entre dominio e infraestructura.

### 🔹 Capa de Infraestructura

- **Propósito**: Implementa adaptadores concretos para sistemas externos.
- **Ubicación**: `app/modules/users/infrastructure/`
- **Contiene**:
  - Modelos de base de datos (`models.py`)
  - Acceso a datos (`repository.py`)
  - Controladores API (`routers/`)

### 🔹 Capa de Interfaces

- **Propósito**: Define contratos para repositorios y adaptadores.
- **Ubicación**: `app/modules/users/interfaces/`
- **Contiene**: Clases base abstractas y protocolos.

### 🔹 Adaptadores de Presentación

- **Propósito**: Transforma entidades internas a representaciones externas.
- **Ubicación**: `app/modules/users/adapters/serializers.py`
- **Contiene**: Modelos Pydantic para serializar entidades de dominio a respuestas API.