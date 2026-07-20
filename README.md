# Automated Web Application Penetration Testing Framework (PortSwigger Academy)

[![Tech Stack](https://shields.io)](https://python.org)
[![Target Stack](https://shields.io)](https://microsoft.com)
[![Security](https://shields.io)](https://owasp.org)

## 🚀 Overview

This repository contains a comprehensive suite of production-grade **Python automation scripts** designed to programmatically exploit, verify, and validate vulnerabilities across all **17 learning paths** of the PortSwigger Web Security Academy. 

Instead of relying solely on manual proxy intervention (Burp Suite GUI), this framework treats security testing as an engineering discipline. Every script is built to simulate automated dynamic application security testing (DAST) and security regression suites—mimicking how modern AppSec teams scale security testing within CI/CD pipelines.

---

## 🛠️ Engineered Tech Stack

*   **Automation Engine:** Python 3.x (`requests`, `BeautifulSoup4`, `asyncio` for multi-threaded testing)
*   **Target Core Knowledge:** Deep alignment with secure engineering patterns across **C# .NET Core, and Angular frontends**.
*   **Vulnerability Domains Covered:** 100% of the OWASP Top 10 including advanced exploitation of business logic flaws, request smuggling, asynchronous SSRF, and JWT bypasses.

---

## 📂 Repository Structure & Covered Paths

The repository is modularly structured by vulnerability domain. Each directory contains the exploit payload logic, a automated exploit script, and documentation on the code-level remediation.

PortSwiggerAcademy
├── 1-Directory-Traversal/    # Automation of path canonicalization bypasses
```
---

## 💡 Engineering Highlights & Design Patterns

### 1. Robust Session & CSRF Handling
Web vulnerability scripting often breaks due to dynamic anti-CSRF tokens. These scripts implement real-time HTML parsing using `BeautifulSoup` to extract context-dependent tokens (like Angular tokens or ASP.NET `__RequestVerificationToken`) dynamically before transmitting attack payloads.

### 2. Blind Exploitation Automation
For data exfiltration via blind SQLi or conditional errors, the scripts implement optimized binary search algorithms and time-delay calculations in Python to reduce network overhead and extract databases efficiently.

### 3. Focus on Code-Level Remediation
This repository does not just focus on the offensive side. Every automated script's folder includes architectural notes on how to patch the underlying issue in enterprise environments—focusing heavily on safe framework implementations like **Entity Framework Core (LINQ/Parameterized queries)** for data access and native cloud secure configurations in **Azure**.

---

## 🔧 Setup & Usage

Ensure you have your academy laboratory active, target URL configured, and your local environment variables set up if proxying through Burp Suite for debugging.

```bash
# Clone the automation framework
git clone https://github.com
cd PortSwiggerAcademy

# Run an automated exploit validation script
python3 directory-traversal-lab-01.py "https://web-security-academy.net"
```

---

## 👨‍💻 About Me

I am a **Mid-Level Application Security Engineer** specializing in full-stack security engineering (.NET, Python, Angular) and Azure cloud deployments. I bridge the gap between development teams and security operations by translating complex vulnerabilities into clean, developer-friendly code remediation strategies and scalable DevSecOps automation.
