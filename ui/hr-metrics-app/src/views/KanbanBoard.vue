<template>
  <div class="kanban-board">
    <h1>Kanban Board</h1>
    <div class="column todo">
      <header>TODO</header>
      <ul class="cards">
        <li v-for="task in tasks" :key="task.uuid">
          <button type="button" @click="handleMove(task)" :class="{ done: task.status === 'completed', inprogress: task.status === 'pending' }">
            {{ task.description }}
          </button>
        </li>
      </ul>
    </div>
    <div class="column inprogress">
      <header>В ПРОЦЕССЕ</header>
      <ul class="cards">
        <li v-for="task in pendingTasks" :key="task.uuid">
          <button type="button" @click="handleMove(task)" :class="{ done: task.status === 'completed', inprogress: task.status === 'pending' }">
            {{ task.description }}
          </button>
        </li>
      </ul>
    </div>
    <div class="column done">
      <header>ГОТОВО</header>
      <ul class="cards">
        <li v-for="task in completedTasks" :key="task.uuid">
          <button type="button" @click="handleMove(task)" :class="{ done: task.status === 'completed', inprogress: task.status === 'pending' }">
            {{ task.description }}
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tasks: [],
      pendingTasks: [],
      completedTasks: []
    };
  },
  computed: {
    allTasks() {
      return this.tasks.concat(this.pendingTasks).concat(this.completedTasks);
    }
  },
  methods: {
    handleMove(task) {
      const newColumnIndex = this.allTasks.findIndex(t => t.uuid === task.uuid);


      if (newColumnIndex >= this.tasks.length) {
        this.tasks.push(task);
      } else if (newColumnIndex >= this.pendingTasks.length && newColumnIndex < this.tasks.length) {
        this.pendingTasks.push(task);
      } else if (newColumnIndex >= this.completedTasks.length && newColumnIndex < this.pendingTasks.length) {
        this.completedTasks.push(task);
      }


      if (newColumnIndex === this.tasks.length - 1) {
        this.tasks.pop();
      } else if (newColumnIndex === this.pendingTasks.length - 1) {
        this.pendingTasks.pop();
      } else if (newColumnIndex === this.completedTasks.length - 1) {
        this.completedTasks.pop();
      }
    }
  },
  created() {
    let data = [
        {
          "uuid": "e533214b-60e0-4af3-a437-af4dcb4b95cc",
          "type": "interview",
          "recruiter_id": 3,
          "description": "Provide morning use total. Learn will direction financial economic. Community soldier this American section current concern focus.",
          "status": "completed",
          "priority": 1,
          "created_at": "2024-04-24T00:00:00",
          "started_at": "2024-06-12T00:00:00",
          "closed_at": "2024-08-17T00:00:00",
          "recruiter": {
            "uuid": "1cb9d379-753a-41c6-9caa-3e2b9f263f6e",
            "id": 3,
            "name": "Douglas Stone",
            "email": "keith96@example.net",
            "role": "developer",
            "phone": "844.613.5114x8497",
            "is_verified": true,
            "is_active": true,
            "grade": 2,
            "efficiently": 3
          }
        },
        {
          "uuid": "6fac8625-8927-446e-a59e-daea9f010f73",
          "type": "interview",
          "recruiter_id": 3,
          "description": "Life generation fund pressure bill successful hotel. Develop what hit. Development land member know anyone how.",
          "status": "completed",
          "priority": 5,
          "created_at": "2024-04-04T00:00:00",
          "started_at": "2024-08-07T00:00:00",
          "closed_at": "2024-09-23T00:00:00",
          "recruiter": {
            "uuid": "1cb9d379-753a-41c6-9caa-3e2b9f263f6e",
            "id": 3,
            "name": "Douglas Stone",
            "email": "keith96@example.net",
            "role": "developer",
            "phone": "844.613.5114x8497",
            "is_verified": true,
            "is_active": true,
            "grade": 2,
            "efficiently": 3
          }
        },
        {
          "uuid": "bf12ee24-0dfd-43fc-89b4-f6122a9eca13",
          "type": "follow-up",
          "recruiter_id": 6,
          "description": "Rule on happy director civil note. Everyone plant fish front food make lawyer.\nI heart gas according. Apply road might.\nAs two benefit as leg. Food free piece theory black determine black name.",
          "status": "pending",
          "priority": 2,
          "created_at": "2024-07-21T00:00:00",
          "started_at": "2024-01-21T00:00:00",
          "closed_at": "2024-02-05T00:00:00",
          "recruiter": {
            "uuid": "71beb833-e127-42ab-b57a-183cb8aa313f",
            "id": 6,
            "name": "Christina Terry",
            "email": "michael85@example.net",
            "role": "recruiter",
            "phone": "(597)508-2928",
            "is_verified": false,
            "is_active": true,
            "grade": 2,
            "efficiently": 3
          }
        },
        {
          "uuid": "569b5a22-579c-4dcf-9099-b5a8fb187640",
          "type": "interview",
          "recruiter_id": 6,
          "description": "Task bit much. Grow personal from. Like ball until want. Real play garden contain activity.\nCommunity lot song both activity society. Reflect debate especially lay.",
          "status": "open",
          "priority": 1,
          "created_at": "2024-07-01T00:00:00",
          "started_at": "2024-09-06T00:00:00",
          "closed_at": "2024-08-24T00:00:00",
          "recruiter": {
            "uuid": "71beb833-e127-42ab-b57a-183cb8aa313f",
            "id": 6,
            "name": "Christina Terry",
            "email": "michael85@example.net",
            "role": "recruiter",
            "phone": "(597)508-2928",
            "is_verified": false,
            "is_active": true,
            "grade": 2,
            "efficiently": 3
          }
        },
        {
          "uuid": "d5532f7d-56c5-4d1f-bfac-3edfd553595f",
          "type": "interview",
          "recruiter_id": 7,
          "description": "Medical for two position nearly beat gas open. Green total town tree. Project mother law cold try.\nFloor risk either require thought wait project stage. Billion information get organization.",
          "status": "pending",
          "priority": 2,
          "created_at": "2024-03-30T00:00:00",
          "started_at": "2024-05-30T00:00:00",
          "closed_at": "2024-09-14T00:00:00",
          "recruiter": {
            "uuid": "ff976d8d-decd-4c5d-a8e8-08a9a22c0c72",
            "id": 7,
            "name": "Brenda Little",
            "email": "tjohnson@example.org",
            "role": "developer",
            "phone": "8916437472",
            "is_verified": false,
            "is_active": true,
            "grade": 3,
            "efficiently": 1
          }
        }

    ]
        this.tasks = data.filter(task => task.status === 'pending').map(task => ({ ...task, status: '' }));
        this.pendingTasks = data.filter(task => task.status === 'inprogress').map(task => ({ ...task, status: '' }));
        this.completedTasks = data.filter(task => task.status === 'completed').map(task => ({ ...task, status: '' }));
  }
};
</script>

<style scoped>
.kanban-board {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding: 1em;
}

.column {
  background-color: #fafafa;
  border: 1px solid rgba(0, 0, 0, 0.125);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 0.5rem;
  padding: 1em;
  width: 20%;
}

.column header {
  font-size: 1.2em;
  text-align: center;
  margin-bottom: 1em;
}

.cards {
  list-style: none;
  padding: 0;
}

.card {
  background-color: white;
  border: 1px solid rgba(0, 0, 0, 0.125);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  padding: 1em;
  text-align: center;
}

.card button {
  width: 100%;
  height: 100%;
  padding: 0;
  border: none;
  outline: none;
  background: transparent;
  cursor: pointer;
}

.card button::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.2s ease-out;
}

.card button:hover::before {
  opacity: 0.2;
}

.card button:active::before {
  opacity: 0.4;
}

.card button:focus::before {
  opacity: 0.6;
}

.card.done button::before {
  background-color: green;
}

.card.inprogress button::before {
  background-color: orange;
}
</style>