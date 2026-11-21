<template>
  <div class="space-y-3">
    <h3 class="text-sm font-semibold text-slate-700 flex items-center gap-2">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
      </svg>
      待办事项
      <span class="text-slate-400 font-normal">（{{ todos.length }} 项）</span>
    </h3>

    <div v-if="todos.length === 0" class="text-sm text-slate-400 py-2">
      暂无待办事项
    </div>

    <div
      v-for="(todo, index) in todos"
      :key="index"
      class="flex items-start gap-3 bg-slate-50 rounded-lg p-3 border border-slate-100"
    >
      <!-- 序号 -->
      <span class="w-6 h-6 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-xs font-semibold shrink-0 mt-0.5">
        {{ index + 1 }}
      </span>

      <!-- 任务内容 -->
      <div class="flex-1 min-w-0">
        <p class="text-sm text-slate-800 font-medium">{{ todo.task }}</p>
        <div class="flex items-center gap-3 mt-1 text-xs text-slate-500">
          <span class="flex items-center gap-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            {{ todo.assignee }}
          </span>
          <span class="flex items-center gap-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            {{ todo.deadline }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TodoItem } from '@/types'

defineProps<{
  todos: TodoItem[]
}>()
</script>
