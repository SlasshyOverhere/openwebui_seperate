<script lang="ts">
	import { getContext } from 'svelte';
	const i18n = getContext('i18n');
</script>

<div class="flex flex-col h-full justify-center items-center text-center p-8">
	<div class="max-w-md">
		<div class="mb-4">
			<svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
		</div>
		
		<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
			{$i18n.t('Backend-Managed Configuration')}
		</h3>
		
		<p class="text-sm text-gray-500 dark:text-gray-400 mb-4">
			{$i18n.t('This OpenWebUI instance is configured as a backend-only system. All API keys and model configurations are managed server-side via environment variables.')}
		</p>
		
		<div class="bg-gray-50 dark:bg-gray-800 rounded-lg p-4 text-left">
			<p class="text-xs text-gray-600 dark:text-gray-300 mb-2">
				<strong>{$i18n.t('To configure API keys:')}</strong>
			</p>
			<ol class="text-xs text-gray-600 dark:text-gray-300 list-decimal list-inside space-y-1">
				<li>{$i18n.t('Edit the backend .env file')}</li>
				<li>{$i18n.t('Set OPENAI_API_KEY=your-key-here')}</li>
				<li>{$i18n.t('Restart the backend server')}</li>
			</ol>
		</div>
		
		<p class="text-xs text-gray-400 dark:text-gray-500 mt-4">
			{$i18n.t('No frontend configuration required. Models will appear automatically after backend setup.')}
		</p>
	</div>
</div>
