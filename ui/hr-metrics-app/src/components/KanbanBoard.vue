<template>
  <KanbanBoard :columns="['To Do', 'In Progress', 'Done']">
    <template #column="props">
      <div class="card" :class="{'is-selected': props.column === activeColumn}" @click="selectColumn(props.column)">
        {{ props.column }}
        <slot name="cards" :column="props.column" />
      </div>
    </template>

    <template #cards="props">
      <div v-for="(card, index) in props.column.cards" :key="index" class="card" @dragstart="onDragStart" @drop="onDrop">
        <div class="card-header" draggable="true">{{ card.title }}</div>
        <div class="card-content">{{ card.description }}</div>
      </div>
    </template>
  </KanbanBoard>
</template>

<script>
import { reactive } from 'vue';
import KanbanBoard from './KanbanBoard.vue';

export default {
  name: 'App',
  components: {
    KanbanBoard
  },
  setup() {
    const state = reactive({
      cards: [],
      activeColumn: null
    });

    function generateCards() {
      const numberOfCards = Math.floor(Math.random() * 20) + 1; // от 1 до 20
      for (let i = 0; i < numberOfCards; i++) {
        state.cards.push({
          title: faker.lorem.words(),
          description: faker.lorem.paragraphs(),
          color: ['primary', 'info', 'success', 'warning', 'danger'][Math.floor(Math.random() * 5)]
        });
      }
    }

    function selectColumn(column) {
      state.activeColumn = column;
    }

    function onDragStart(event) {
      event.dataTransfer.setData('text', event.target.className);
    }

    function onDrop(event) {
      if (event.preventDefault) {
        event.preventDefault();
      }
      const data = event.dataTransfer.getData('text');
      const cardElement = document.querySelector(`div.${data}`);
      if (!cardElement || !event.target.className) {
        return;
      }
      cardElement.classList.remove(data);
      cardElement.classList.add(event.target.className);

      const sourceColumn = state.columns.find((col) => col.name === 'To Do');
      const targetColumn = state.columns.find((col) => col.name === 'Done');
      if (sourceColumn && targetColumn) {
        sourceColumn.cards.splice(sourceColumn.cards.indexOf(cardElement), 1);
        targetColumn.cards.push(cardElement);
      }
    }

    watchEffect(() => {
      generateCards();
    });

    return {
      state,
      selectColumn
    };
  },
};
</script>