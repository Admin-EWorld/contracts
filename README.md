# ContractPro - Professional International Contract Generator

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

**Professional service agreement generator with multi-currency support, international legal compliance, and modern UI.**

---

## 🌟 Features

### Core Functionality
- ✅ **Multi-Currency Support** - USD, EUR, GBP, AED, SAR with automatic conversion
- ✅ **Multiple Export Formats** - Generate contracts as DOCX or PDF
- ✅ **Contract Management** - Store, search, and manage all contracts
- ✅ **International Compliance** - Templates designed for global use
- ✅ **Professional UI** - Modern, responsive design with dark mode
- ✅ **Real-time Validation** - Client and server-side form validation
- ✅ **Contract Preview** - Review before generation
- ✅ **Database Storage** - SQLite database for contract history

### Service Types
- 💰 **Finance & Accounting** - Bookkeeping, financial reporting, tax advisory
- 💻 **IT & Software** - Development, infrastructure, cloud services
- 👥 **HR & Payroll** - Payroll processing, employee management
- 📊 **Business Consulting** - Strategic planning, operations, growth

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Admin-EWorld/contracts.git
   cd contracts
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 4000 --reload
   ```

5. **Open in browser**
   ```
   http://localhost:4000
   ```

---

## 📁 Project Structure

```
contracts/
├── main.py                 # Main FastAPI application
├── database.py             # SQLAlchemy database models
├── pdf_generator.py        # PDF generation module
├── requirements.txt        # Python dependencies
├── contracts.db           # SQLite database (auto-generated)
│
├── static/
│   ├── css/
│   │   └── main.css       # Professional design system
│   ├── js/
│   │   └── main.js        # Client-side validation & interactivity
│   └── images/
│
├── templates/
│   ├── base.html          # Base template
│   ├── pages/
│   │   ├── home.html      # Contract generation form
│   │   ├── contracts.html # Contract management
│   │   └── about.html     # About page
│   └── master_contract.docx # DOCX template
│
├── clauses/
│   ├── finance.txt        # Finance services clause
│   ├── it.txt            # IT services clause
│   ├── hr.txt            # HR services clause
│   └── business.txt      # Business consulting clause
│
└── generated/            # Generated contract files
```

---

## 🎯 Usage

### Creating a Contract

1. **Fill in Client Information**
   - Client name
   - Country/jurisdiction
   - Contract duration

2. **Set Financial Terms**
   - Fee amount
   - Currency selection
   - Automatic USD conversion displayed

3. **Select Services**
   - Choose one or more service types
   - Each adds specific clauses to contract

4. **Preview & Generate**
   - Preview contract details
   - Generate DOCX or PDF

### Managing Contracts

- **View All Contracts** - Navigate to "My Contracts"
- **Search & Filter** - By client name, country, or currency
- **Download** - Re-download as DOCX or PDF
- **View Details** - See full contract information

---

## 🔧 Configuration

### Currency Rates
Edit `CURRENCIES` in `main.py` to update exchange rates:

```python
CURRENCIES = {
    "USD": {"symbol": "$", "name": "US Dollars", "rate": 1},
    "EUR": {"symbol": "€", "name": "Euros", "rate": 1.08},
    # Add more currencies...
}
```

### Service Clauses
Edit files in `clauses/` directory to customize service descriptions:
- `finance.txt` - Finance & Accounting services
- `it.txt` - IT & Software services
- `hr.txt` - HR & Payroll services
- `business.txt` - Business Consulting services

### Master Template
Edit `templates/master_contract.docx` to customize the contract template layout.

---

## 🌐 API Endpoints

### Public Endpoints
- `GET /` - Home page with contract form
- `GET /contracts` - Contract management page
- `GET /about` - About page
- `POST /generate` - Generate new contract

### API Endpoints
- `GET /api/contract/{id}` - Get contract details
- `GET /download/{id}/{format}` - Download contract (docx/pdf)
- `DELETE /api/contract/{id}` - Delete contract
- `GET /api/stats` - Get contract statistics
- `GET /health` - Health check

---

## 🔒 Security & Compliance

### Data Protection
- All data stored locally in SQLite database
- No third-party data sharing
- Secure file storage in `generated/` directory

### Legal Disclaimer
⚠️ **Important**: These contracts are templates for general use. Always have contracts reviewed by a qualified legal professional in your jurisdiction before execution. ContractPro does not provide legal advice.

### Compliance Features
- GDPR-compliant data handling
- International accounting standards (IFRS/GAAP) references
- Jurisdiction-specific disclaimers
- Intellectual property clauses
- Confidentiality provisions

---

## 🎨 Design System

### Color Palette
- **Primary**: Professional blue (#1e40af)
- **Secondary**: Teal (#0f766e)
- **Accent**: Amber (#d97706)
- **Success**: Green (#059669)
- **Error**: Red (#dc2626)

### Features
- Responsive design (mobile, tablet, desktop)
- Dark mode support
- Smooth animations and transitions
- Accessible UI components
- Professional typography (Inter font)

---

## 📊 Database Schema

### Contract Table
```sql
- id (Primary Key)
- client_name
- country
- fees, fees_numeric, fees_words
- currency, currency_symbol, currency_name
- usd_equivalent
- contract_duration
- services
- effective_date
- file_path, file_id
- created_at, updated_at
```

---

## 🛠️ Development

### Running in Development Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 4000 --reload
```

### Running in Production
```bash
uvicorn main:app --host 0.0.0.0 --port 4000 --workers 4
```

### Adding New Service Types

1. Create clause file in `clauses/` directory
2. Add checkbox in `templates/pages/home.html`
3. Update service descriptions in About page

---

## 📝 Version History

### Version 2.0 (Current)
- ✅ Complete UI redesign with modern design system
- ✅ Database-backed contract management
- ✅ PDF export functionality
- ✅ Advanced search and filtering
- ✅ Real-time form validation
- ✅ Currency conversion display
- ✅ Contract preview modal
- ✅ Dark mode support
- ✅ Enhanced legal compliance
- ✅ Responsive design

### Version 1.0
- Basic contract generation
- DOCX export only
- Simple HTML form
- Multi-currency support
- Service clause templates

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI inspired by modern design systems
- Legal templates based on international standards
- PDF generation with [ReportLab](https://www.reportlab.com/)

---

## 📧 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

## 🔮 Roadmap

### Planned Features
- [ ] Digital signature integration
- [ ] Email delivery system
- [ ] Multi-language support
- [ ] Custom clause builder
- [ ] Contract templates library
- [ ] Analytics dashboard
- [ ] API for external integrations
- [ ] User authentication system
- [ ] Team collaboration features
- [ ] Contract versioning

---

**Made with ❤️ by Admin-EWorld**
