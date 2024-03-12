# Biosecurity
ID: 1159528

### 1. Web Application Structure
1. If not logged in, users can see the homepage, registration, and login pages. If logged in, there are three different roles: forester, staff, and admin, each with its own unique page.
2. Foresters can view the forestry guide page (guide.html), click on images to see details (detail.html), and also modify personal information (profile.html).
3. Staff members can view the forestry guide page (guide.html), click on images to view details and make modifications (detail.html), add new guides (add_guide.html), as well as modify personal information (profile.html) and view the personal information of foresters (f_profile.html).
4. The admin can view the forestry guide page (guide.html), click on images to view details and make modifications (detail.html), add new guides (add_guide.html), as well as modify personal information (profile.html). Additionally, they can view and modify the personal information of foresters (f_profile.html) and staff members (s_profile.html).

### 2. Design Decisions
1. The overall structure is differentiated through blueprints, distinguishing the functional pages for the three roles. User permissions are confirmed using sessions, and passwords are processed using hashing.
2. For information modification, except for adding new guides, both the modification of personal information and the modification of detailed information are presented in pop-up modal boxes.
3. In the modification of personal information, changing the password requires inputting the original password for verification. However, when editing the information of foresters and staff as an admin, password reset can be done without entering the original password. This approach is considered due to the possibility of employees forgetting their passwords.

### 3. References
1. https://esg.gvm.com.tw/article/10903
2. https://www.nzffa.org.nz/farm-forestry-model/the-essentials/forest-health-pests-anddiseases/