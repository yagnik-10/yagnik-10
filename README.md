# Hi there, Yagnik here

[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:yagnik.pavagadhi06@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yagnikpavagadhi)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF6B6B?style=for-the-badge&logo=portfolio&logoColor=white)](https://www.yagnikpavagadhi.com)



---

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=700&size=24&pause=900&color=00D4FF&center=true&vCenter=true&width=780&lines=Hi,+I+am+Yagnik+Pavagadhi;AI%2FML+Engineer+%E2%80%A2+Software+Engineer+%E2%80%A2+Full+Stack;Building+intelligent+systems+and+scalable+solutions" alt="header" />
</div>

---

### About
I'm an AI/ML engineer and software developer with a passion for building intelligent systems and scalable applications. Currently pursuing my Master's in Information Systems at Northeastern University, I specialize in prompt engineering, machine learning, and full-stack development. I enjoy creating systems that think, learn, and solve real-world problems.


💬 **Lets connect** and talk about system architecture, the future of AI, and everything in between
😄 **Pronouns:** He/Him
👾 **Fun fact:** Everything that has been or could be written/said already exists in the [Library of Babel](https://libraryofbabel.info)



```java
@RestController
@RequestMapping("/api/clients")
public class ClientController {
    
    @Autowired
    private ClientService clientService;
    
    @GetMapping("/{id}")
    public ResponseEntity<Client> getClient(@PathVariable String id) {
        // Optimized query with caching
        Client client = clientService.findByIdWithCache(id);
        return ResponseEntity.ok(client);
    }
    
    @PostMapping
    public ResponseEntity<Client> createClient(@RequestBody Client client) {
        // Validation and business logic
        Client saved = clientService.save(client);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }
}
```
</details>

<details>
<summary>Blueprint: React.js Dashboard with Real-time Analytics</summary>

```javascript
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const AnalyticsDashboard = () => {
    const [data, setData] = useState([]);
    
    useEffect(() => {
        // Real-time data fetching with WebSocket
        const ws = new WebSocket('ws://localhost:8080/analytics');
        ws.onmessage = (event) => {
            setData(JSON.parse(event.data));
        };
        
        return () => ws.close();
    }, []);
    
    return (
        <div className="dashboard">
            <h2>Real-time Analytics</h2>
            <LineChart width={600} height={300} data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#8884d8" />
            </LineChart>
        </div>
    );
};
```
</details>

---

<div align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&size=18&pause=1200&color=00D4FF&center=true&vCenter=true&width=720&lines=Open+to+AI%2FML+Engineering+%2C+Software+Engineering+%2C+and+Data+Engineering+roles" alt="footer" />
</div>
