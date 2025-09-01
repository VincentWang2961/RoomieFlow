# Accommodation Scheduling Management System Requirements

## 🚦 Implementation Status
**Current Phase**: MVP Development ✅ COMPLETED  
**Version**: 0.1.0  
**Last Updated**: 2025-01-02  
**Status**: Ready for Testing and Deployment

### ✅ Completed Features
- Complete backend API with Flask and SQLAlchemy
- JWT-based authentication system
- Vue.js frontend with responsive design
- Docker containerization
- User management and role-based access
- Property and room management
- Booking application and approval system
- Time allocation tracking (backend)

### ⏳ Future Enhancements
- Email notification system
- Frontend time tracking dashboard
- Usage warnings and limits visualization
- Calendar integration
- Mobile app development

## Project Overview
A lightweight, web-based accommodation scheduling management system designed for simplicity and ease of use. The system handles accommodation time slot applications and approvals with minimal complexity while maintaining essential functionality for user management, property administration, and flexible time allocation parameters.

**Core Design Principles:**
- Simple and intuitive user experience
- Lightweight architecture with minimal dependencies
- Fast performance and quick deployment
- Clean, modern interface design
- Mobile-first responsive approach

## Functional Requirements

### User Management (Simplified) ✅ COMPLETED
- ✅ Simple user registration with email verification
- ✅ Basic authentication with password requirements
- ✅ Two primary roles: User and Administrator (simplified permission model)
- ✅ Property-based user grouping with minimal permission complexity
- ✅ User profile management with essential information only

### Property and Room Management (Essential Features) ✅ COMPLETED
- ✅ Simple property creation with basic information (name, description)
- ✅ Room management with essential details (name, capacity, availability)
- ⏳ User invitation system via email for property access (FUTURE)
- ✅ Basic administrative controls for property owners
- ✅ Minimal data collection to reduce complexity

### Time Slot Management ✅ COMPLETED
- ✅ Three distinct time periods:
  - Morning session
  - Midday session (includes lunch)
  - Evening session (includes overnight stay)
- ✅ Configurable time duration parameters (e.g., 0.5 or 1 day per session)
- ✅ Weekly time allocation limits (e.g., 7 days per week shared amongst users)

### Application and Approval System ✅ COMPLETED
- ✅ Users can submit accommodation requests for specific time slots
- ✅ Administrator approval workflow
- ✅ Application status tracking (pending, approved, rejected)
- ⏳ Notification system for application updates (FUTURE)

### Time Tracking and Monitoring ⏳ PARTIALLY COMPLETED
- ✅ Real-time calculation of weekly time usage (backend logic ready)
- ✅ Shared time pool management between users
- ⏳ Usage warnings when approaching or exceeding weekly limits (frontend needed)
- ⏳ Non-enforced overtime allowance with warning notifications (frontend needed)

## Technical Requirements

### Technology Stack
**Backend (Lightweight Approach):**
- Flask (preferred for simplicity and minimal overhead)
- RESTful API architecture with minimal endpoints
- SQLAlchemy Core for lightweight database operations
- JWT authentication for stateless, simple token management
- Minimal third-party dependencies to reduce complexity

**Frontend (Lightweight Approach):**
- Vue.js 3 with Composition API for modern, efficient development
- Pinia for lightweight state management (preferred over Vuex for simplicity)
- Vue Router for client-side navigation
- Native Fetch API or Axios for API communication
- Minimal UI framework approach:
  - **Recommended:** Custom CSS with utility classes for maximum performance
  - **Alternative:** Tailwind CSS for rapid, lightweight styling
  - **Component Library:** PrimeVue (if needed) for essential components only
- CSS Grid and Flexbox for responsive layouts without heavy frameworks
- Minimal JavaScript bundle size optimisation

**Database (Lightweight Configuration):**
- **Production:** PostgreSQL (single instance for simplicity)
- **Development:** SQLite for easy setup and testing
- **Caching:** Redis (optional, implement only if performance requires it)
- Database design focused on simplicity with minimal tables and relationships

**Email Services (Mid-to-Late Development Phase):**
- SMTP server integration for email delivery
- Email template system for consistent messaging
- Queue-based email processing for reliability
- Email service options: SendGrid, Mailgun, or self-hosted SMTP

### System Architecture (Lightweight Design)
- Single Page Application (SPA) frontend for fast user experience
- RESTful API backend with minimal service separation
- JWT token-based authentication (no session storage required)
- Real-time notifications via Server-Sent Events (simpler than WebSocket)
- Minimal microservice architecture - monolithic backend for simplicity
- Static file serving directly from web server (no CDN complexity initially)

## Data Models (Simplified Schema)

### User (Essential Fields Only)
- User ID (UUID), username, email, password hash
- Role (enum: 'user', 'admin')
- Created timestamp, last login
- Email verification status

### Property (Minimal Information)
- Property ID (UUID), name, description
- Owner user ID, creation timestamp
- Simple status (active/inactive)

### PropertyMember (User-Property Relationship)
- Property ID, user ID, role within property
- Invitation status, joined timestamp

### Room (Basic Details)
- Room ID (UUID), property ID, name
- Capacity (integer), description
- Active status

### BookingApplication (Core Booking Data)
- Application ID (UUID), user ID, room ID
- Date, session type (morning/midday/evening)
- Status (pending/approved/rejected), notes
- Created/updated timestamps, duration value

### TimeAllocation (Weekly Limits)
- Property ID, weekly limit (days)
- Session duration mapping (morning: 0.5, midday: 1.0, evening: 1.0)
- Reset day of week (e.g., Monday)

**Database Design Principles:**
- Minimal foreign key relationships
- Simple data types (avoid complex JSON fields initially)
- Efficient indexing on commonly queried fields
- Single timezone handling (UTC storage, local display)

## User Interface Requirements

### Dashboard
- Clean and organised overview of current applications with visual status indicators
- Interactive weekly time usage summary with progress bars and charts
- Quick application submission with streamlined form design
- Upcoming bookings calendar with mobile-optimised date picker
- Card-based layout for easy scanning and interaction
- Responsive grid system that adapts from multi-column (desktop) to single-column (mobile)

### Application Management
- Intuitive multi-step form for submitting accommodation requests
- Visual application history with timeline view and status badges
- Easy-to-use editing interface for pending applications
- One-tap booking cancellation with clear confirmation dialogs
- Swipe gestures for mobile interactions (approve/reject, edit/delete)
- Collapsible sections and accordions for efficient space usage on mobile

### Administrative Interface
- Streamlined application review interface with quick approve/reject actions
- Drag-and-drop user management with role assignment
- Visual time allocation parameter configuration with slider controls
- Mobile-friendly data tables with horizontal scrolling and filtering
- Export functionality with multiple format options (PDF, CSV, Excel)
- Responsive sidebar navigation that collapses to hamburger menu on mobile

### Notifications
- Real-time application status updates
- Weekly usage limit warnings
- Upcoming booking reminders
- Email notification system (planned for mid-to-late development phase):
  - Administrator email alerts for new accommodation applications
  - User email notifications for application approvals/rejections
  - Weekly usage summary emails
  - Booking reminder emails

## Non-Functional Requirements

### Performance (Lightweight Targets)
- Support 50-100 concurrent users (suitable for typical accommodation management)
- Page load times under 1.5 seconds (optimised for simplicity)
- Real-time updates within 2 seconds (acceptable for accommodation booking use case)
- Minimal JavaScript bundle size (< 500KB gzipped)
- Database queries optimised for common use cases
- Efficient API endpoint design with minimal data transfer

### Security
- Secure password storage (bcrypt hashing)
- Input validation and sanitisation
- SQL injection prevention
- Cross-site scripting (XSS) protection
- Australian Privacy Principles compliance

### Usability and User Experience
- Clean, modern, and aesthetically pleasing interface design
- Simple and intuitive navigation with minimal learning curve
- Elegant and professional visual design language
- Mobile-first responsive design approach
- Seamless experience across desktop, tablet, and mobile devices
- Touch-friendly interface elements for mobile users
- Optimised layouts for different screen sizes and orientations
- Australian English localisation throughout the application
- Accessibility compliance (WCAG 2.1 AA standards)
- Clear and helpful error messaging with actionable guidance
- Consistent visual hierarchy and typography

## Deployment and Infrastructure

### Version Control and Project Management
- GitHub repository for source code management
- Git workflow with feature branches and pull requests
- Issue tracking and project management via GitHub Issues/Projects
- Automated testing and CI/CD integration with GitHub Actions

### Containerisation and Deployment (Lightweight Setup)
- Docker containerisation for easy deployment and consistency
- Simple Docker Compose configuration for development
- Minimal container architecture:
  - **Frontend:** Static files served by Nginx
  - **Backend:** Single Flask application container
  - **Database:** PostgreSQL container
  - **Reverse Proxy:** Traefik (for automatic SSL and routing)
- Optional Redis container (add only if caching becomes necessary)
- Single-file environment configuration for easy management

### Home Server Infrastructure
- Self-hosted deployment on home server with public IP
- Domain management through Cloudflare DNS
- Multi-domain routing for different applications:
  - Main application: `accommodation.example.com`
  - Alternative subdomain: `schedule.example.com`
  - Admin panel: `admin-accommodation.example.com`

### Reverse Proxy Configuration (Simplified)
**Traefik (Recommended for Simplicity):**
- Automatic SSL certificate generation and renewal
- Simple Docker label-based routing configuration
- Minimal configuration files
- Built-in health checks and automatic service discovery
- Perfect for home server deployment with multiple domains

**Configuration Example:**
```yaml
# Minimal Traefik setup for lightweight deployment
labels:
  - "traefik.http.routers.app.rule=Host(`accommodation.example.com`)"
  - "traefik.http.routers.app.tls.certresolver=letsencrypt"
```

### Domain and SSL Management
- Cloudflare DNS management with programmatic API access
- SSL certificates via Let's Encrypt (automated renewal)
- Cloudflare proxy for additional security and performance
- DDNS updates for dynamic IP management (if required)

### Container Orchestration
```yaml
# Docker Compose structure example:
services:
  frontend:
    build: ./frontend
    labels:
      - "traefik.http.routers.accommodation.rule=Host(`accommodation.example.com`)"
  
  backend:
    build: ./backend
    labels:
      - "traefik.http.routers.api.rule=Host(`api.accommodation.example.com`)"
  
  database:
    image: postgres:15
    
  redis:
    image: redis:7-alpine
    
  traefik:
    image: traefik:v3.0
    ports:
      - "80:80"
      - "443:443"
```

### Monitoring and Maintenance (Lightweight Approach)
- Basic Docker health checks for service availability
- Simple file-based logging with log rotation
- Daily automated database backups with retention policy
- **Portainer CE** for simple Docker container management via web interface
- Manual container updates with tested rollback procedures
- Essential monitoring only - avoid complex monitoring stacks
- Health check endpoint for external monitoring if needed

### Security Considerations
- Firewall configuration to expose only necessary ports (80, 443)
- Docker security best practices (non-root containers, minimal base images)
- Network isolation between containers
- Regular security updates for base images and dependencies
- Cloudflare security features (DDoS protection, Web Application Firewall)

## Development Methodology

### Agile Development Approach
- Sprint-based development cycles (2-week sprints recommended)
- Regular stakeholder feedback and iterative improvements
- Minimum Viable Product (MVP) delivery followed by feature increments
- Daily stand-ups and sprint retrospectives
- User story-driven development with acceptance criteria

### Development Phases (Lightweight Approach)
**Phase 1 (MVP - Essential Features Only):**
- User registration, login, and basic authentication
- Property creation and room management
- Simple booking application form
- Basic approval/rejection functionality
- Minimal dashboard with current bookings
- Essential time tracking (weekly limits calculation)

**Phase 2 (User Experience Enhancement):**
- Improved interface design and mobile responsiveness
- Real-time status updates via Server-Sent Events
- Enhanced dashboard with usage visualisation
- Simple notification system (in-app only initially)
- Basic booking history and calendar view

**Phase 3 (Communication Integration - Optional):**
- Email notification system (if required by users)
- Simple email templates for applications and approvals
- Basic SMTP integration (self-hosted or service)

**Phase 4 (Polish and Optimisation):**
- Performance optimisation and code refactoring
- Additional convenience features based on user feedback
- Enhanced mobile experience
- Basic reporting features (usage summaries)

**Lightweight Development Principles:**
- Each phase delivers working, deployable software
- Features are added only when genuinely needed
- Maintain simplicity and avoid feature creep
- User feedback drives feature priority

### Continuous Integration/Continuous Deployment (CI/CD)
- Automated testing pipeline with GitHub Actions
- Code quality checks and linting
- Automated deployment to staging environment
- Manual approval process for production deployment

## Email Notification System (Phase 3)

### Email Workflow Implementation
**Application Submission:**
- Trigger: User submits accommodation application
- Action: Send email to designated property administrators
- Content: Application details, applicant information, direct approval/rejection links

**Application Decision:**
- Trigger: Administrator approves or rejects application
- Action: Send email notification to applicant
- Content: Decision status, booking details (if approved), reason for rejection (if applicable)

**Usage Monitoring:**
- Trigger: Weekly usage calculation
- Action: Send summary emails to users and administrators
- Content: Current usage, remaining allocation, upcoming bookings

### Email Service Integration
- Email queue management using Redis or database-based queuing
- Template engine for consistent email formatting (HTML and plain text versions)
- Bounce handling and delivery status tracking
- Email preferences and opt-out functionality
- Testing environment for email workflow verification

## Additional Features and Considerations

### Essential Missing Details Added
**User Experience Enhancements:**
- Simple onboarding flow for new users with guided property setup
- Basic help documentation integrated within the application
- Simple user feedback mechanism for continuous improvement
- Keyboard shortcuts for power users (admin functions)

**Operational Requirements:**
- Simple backup and restore functionality via admin interface
- Basic audit logging for administrative actions
- User account deactivation and data retention policies
- Simple data export functionality (user requests)

**Technical Considerations:**
- Graceful error handling with user-friendly error messages
- Basic API rate limiting to prevent abuse
- Simple health check endpoints for monitoring
- Configuration management via environment variables
- Database migration scripts for version updates

### Future Enhancements (Low Priority)
- Calendar integration (iCal export for approved bookings)
- Basic reporting dashboard with usage statistics
- Multi-language support (if international users needed)
- Mobile app development (only if web app proves insufficient)
- Payment integration (if accommodation requires fees)
- SMS notifications as alternative to email
- Integration with existing property management systems

### Maintenance and Support Considerations
**Documentation Requirements:**
- Simple user manual with screenshots
- Basic administrator guide for property management
- Technical documentation for deployment and maintenance
- API documentation for potential future integrations

**Support Infrastructure:**
- Simple contact form for user support requests
- Basic FAQ section within the application
- Version update notification system
- Simple telemetry for understanding usage patterns (with user consent)

**Scalability Planning (Future):**
- Database optimisation strategies for growth
- Caching implementation when needed
- Load balancing considerations for high traffic
- Multi-tenancy support if serving multiple organisations
