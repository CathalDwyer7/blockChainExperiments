# Brainstorming
We spent a long time brain storming ideas for our year long project and found it difficult to settle on just one idea. We eventually ended up agreeing that a blockchain based voting system is both challenging and interesting enough to warrant us taking it on as our 3rd year project.

# 14/10/2024 Initial pitch to supervisor on our idea
Had our first meeting with Geoff Hamiliton our first choice supervisor. We pitched the idea of a blockchain based voting system. Geoff was very enthusiastic about the idea. He recommended doing further research on both pallier encryption and blind signitures. He also thought that it might be interesting if we did some research on different voting systems. He recommended a quadratic voting system. He agreed to be our supervisor.

# 18/10/2024 Submission of project proposal
We ended up going with a quadratic based voting system as we found it hadnt been fully implemented in many places. We wrote up our project proposal and we were happy with our submission making minor tweaks to our proposal doc in the days leading up to our project proposal submission.

# 31-10-2024 Project approval
Our project was approved by John Mckenna and Ray Walshe. They wanted to know how we would encrypt the votes. We forgot to mention pallier encryption. But we still got our project approved. We showed great understanding of what blockchain is and how blockchain based quadratic voting might be beneficial.

# 03-01-2025 Began coding the project
Added in a basic react Frontend including a page for the admin, voters and a result page. We also mafe a login page to ask the user to login and a dashboard page. Basic outline of the frontend.

# 04-01-2025 Admin and User functionality
Admins can now create, delete and end an election. Users can now cast a vote onto the basic election system.(only frontend functionality currently) Began doing further research on how we can implement blind signitures and paillier encryption for the backend.

# 10-01-2025 Began working on the backend
Setup a backend skeleton to begin development the day after.

# 11-01-2025 
Created basic backend routes for elections and authentification. 

# 13-01-2025
Made more progress on the backend. We made a basic outline for the models we will use in the database while authticating things. As well as a basic routing system that we can test the endpoints of.

# 14-01-2025 testing endpoints
Continued working on the backend end points and got them to pass a few test on postman. A pytest file was also added so the test can be run while in vscode.

# 18-01-2025 Blockchain
Began coding up the logic behind the Blockchain. Added paillier encryption and blind signitures to it. The blockchain works and can use paillier encryption and blind signitures.

# 20-01-2025
Did more testing on the backend and blockchain. Changed the way the chain generates its keys.

# 28-01-2025
Did more testing and rearranged our file structure so that it was easier to understand where issues may occur. Created tests within the modules.
