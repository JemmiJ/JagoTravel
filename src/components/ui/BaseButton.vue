<template>
  <button
    :class="[
      'btn',
      variant === 'primary' && 'btn-primary',
      variant === 'secondary' && 'btn-secondary',
      variant === 'outline' && 'btn-outline',
      variant === 'ghost' && 'btn-ghost',
      variant === 'success' && 'btn-success',
      variant === 'error' && 'btn-error',
      variant === 'warning' && 'btn-warning',
      size === 'sm' && 'btn-sm',
      size === 'md' && 'btn-md',
      size === 'lg' && 'btn-lg',
      size === 'icon' && 'btn-icon',
      block && 'w-full',
      className,
    ]"
    v-bind="$attrs"
  >
    <slot />
  </button>
</template>

<script setup>
defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  block: { type: Boolean, default: false },
  className: { type: String, default: '' },
})
</script>