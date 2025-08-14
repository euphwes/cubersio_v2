<!--
@component

Vertical spacer with predefined sizes.

Props:
- `size`: One of "xs", "s", "m", "l", or "xl"
-->

<script lang="ts">
  type Size = 'xs' | 's' | 'm' | 'l' | 'xl';

  const { size = 'm' }: { size: Size } = $props();

  const sizeMap: Record<Size, string> = {
    xs: '0.25rem',
    s: '0.5rem',
    m: '1rem',
    l: '1.5rem',
    xl: '2rem'
  };
</script>

<div style="height: {sizeMap[size]}; width: 100%;" aria-hidden="true"></div>
