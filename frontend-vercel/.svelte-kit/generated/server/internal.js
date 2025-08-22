
import root from '../root.svelte';
import { set_building, set_prerendering } from '__sveltekit/environment';
import { set_assets } from '__sveltekit/paths';
import { set_manifest, set_read_implementation } from '__sveltekit/server';
import { set_private_env, set_public_env } from '../../../node_modules/@sveltejs/kit/src/runtime/shared-server.js';

export const options = {
	app_template_contains_nonce: false,
	csp: {"mode":"auto","directives":{"upgrade-insecure-requests":false,"block-all-mixed-content":false},"reportOnly":{"upgrade-insecure-requests":false,"block-all-mixed-content":false}},
	csrf_check_origin: true,
	csrf_trusted_origins: [],
	embedded: false,
	env_public_prefix: 'PUBLIC_',
	env_private_prefix: '',
	hash_routing: false,
	hooks: null, // added lazily, via `get_hooks`
	preload_strategy: "modulepreload",
	root,
	service_worker: false,
	service_worker_options: undefined,
	templates: {
		app: ({ head, body, assets, nonce, env }) => "<!doctype html>\n<html lang=\"en\">\n\t<head>\n\t\t<meta charset=\"utf-8\" />\n\t\t<link rel=\"icon\" type=\"image/png\" href=\"/static/favicon.png\" />\n\t\t<link rel=\"icon\" type=\"image/png\" href=\"/static/favicon-96x96.png\" sizes=\"96x96\" />\n\t\t<link rel=\"icon\" type=\"image/svg+xml\" href=\"/static/favicon.svg\" />\n\t\t<link rel=\"shortcut icon\" href=\"/static/favicon.ico\" />\n\t\t<link rel=\"apple-touch-icon\" sizes=\"180x180\" href=\"/static/apple-touch-icon.png\" />\n\t\t<meta name=\"apple-mobile-web-app-title\" content=\"Open WebUI\" />\n\n\t\t<link rel=\"manifest\" href=\"/manifest.json\" crossorigin=\"use-credentials\" />\n\t\t<meta\n\t\t\tname=\"viewport\"\n\t\t\tcontent=\"width=device-width, initial-scale=1, maximum-scale=1, viewport-fit=cover\"\n\t\t/>\n\t\t<meta name=\"theme-color\" content=\"#171717\" />\n\t\t<meta name=\"robots\" content=\"noindex,nofollow\" />\n\t\t<meta name=\"description\" content=\"Open WebUI\" />\n\t\t<link\n\t\t\trel=\"search\"\n\t\t\ttype=\"application/opensearchdescription+xml\"\n\t\t\ttitle=\"Open WebUI\"\n\t\t\thref=\"/opensearch.xml\"\n\t\t/>\n\t\t<script src=\"/static/loader.js\" defer></script>\n\t\t<link rel=\"stylesheet\" href=\"/static/custom.css\" />\n\n\t\t<script>\n\t\t\tfunction resizeIframe(obj) {\n\t\t\t\tobj.style.height = obj.contentWindow.document.documentElement.scrollHeight + 'px';\n\t\t\t}\n\t\t</script>\n\n\t\t<script>\n\t\t\t// On page load or when changing themes, best to add inline in `head` to avoid FOUC\n\t\t\t(() => {\n\t\t\t\tconst metaThemeColorTag = document.querySelector('meta[name=\"theme-color\"]');\n\t\t\t\tconst prefersDarkTheme = window.matchMedia('(prefers-color-scheme: dark)').matches;\n\n\t\t\t\tif (!localStorage?.theme) {\n\t\t\t\t\tlocalStorage.theme = 'system';\n\t\t\t\t}\n\n\t\t\t\tif (localStorage.theme === 'system') {\n\t\t\t\t\tdocument.documentElement.classList.add(prefersDarkTheme ? 'dark' : 'light');\n\t\t\t\t\tmetaThemeColorTag.setAttribute('content', prefersDarkTheme ? '#171717' : '#ffffff');\n\t\t\t\t} else if (localStorage.theme === 'oled-dark') {\n\t\t\t\t\tdocument.documentElement.style.setProperty('--color-gray-800', '#101010');\n\t\t\t\t\tdocument.documentElement.style.setProperty('--color-gray-850', '#050505');\n\t\t\t\t\tdocument.documentElement.style.setProperty('--color-gray-900', '#000000');\n\t\t\t\t\tdocument.documentElement.style.setProperty('--color-gray-950', '#000000');\n\t\t\t\t\tdocument.documentElement.classList.add('dark');\n\t\t\t\t\tmetaThemeColorTag.setAttribute('content', '#000000');\n\t\t\t\t} else if (localStorage.theme === 'light') {\n\t\t\t\t\tdocument.documentElement.classList.add('light');\n\t\t\t\t\tmetaThemeColorTag.setAttribute('content', '#ffffff');\n\t\t\t\t} else if (localStorage.theme === 'her') {\n\t\t\t\t\tdocument.documentElement.classList.add('her');\n\t\t\t\t\tmetaThemeColorTag.setAttribute('content', '#983724');\n\t\t\t\t} else {\n\t\t\t\t\tdocument.documentElement.classList.add('dark');\n\t\t\t\t\tmetaThemeColorTag.setAttribute('content', '#171717');\n\t\t\t\t}\n\n\t\t\t\twindow.matchMedia('(prefers-color-scheme: dark)').addListener((e) => {\n\t\t\t\t\tif (localStorage.theme === 'system') {\n\t\t\t\t\t\tif (e.matches) {\n\t\t\t\t\t\t\tdocument.documentElement.classList.add('dark');\n\t\t\t\t\t\t\tdocument.documentElement.classList.remove('light');\n\t\t\t\t\t\t\tmetaThemeColorTag.setAttribute('content', '#171717');\n\t\t\t\t\t\t} else {\n\t\t\t\t\t\t\tdocument.documentElement.classList.add('light');\n\t\t\t\t\t\t\tdocument.documentElement.classList.remove('dark');\n\t\t\t\t\t\t\tmetaThemeColorTag.setAttribute('content', '#ffffff');\n\t\t\t\t\t\t}\n\t\t\t\t\t}\n\t\t\t\t});\n\t\t\t\tconst isDarkMode = document.documentElement.classList.contains('dark');\n\n\t\t\t\tconst logo = document.createElement('img');\n\t\t\t\tlogo.id = 'logo';\n\t\t\t\tlogo.style =\n\t\t\t\t\t'position: absolute; width: auto; height: 6rem; top: 44%; left: 50%; transform: translateX(-50%); display:block;';\n\t\t\t\tlogo.src = isDarkMode ? '/static/splash-dark.png' : '/static/splash.png';\n\n\t\t\t\tdocument.addEventListener('DOMContentLoaded', function () {\n\t\t\t\t\tconst splash = document.getElementById('splash-screen');\n\t\t\t\t\tif (document.documentElement.classList.contains('her')) {\n\t\t\t\t\t\treturn;\n\t\t\t\t\t}\n\n\t\t\t\t\tif (splash) splash.prepend(logo);\n\t\t\t\t});\n\t\t\t})();\n\t\t</script>\n\n\t\t<title>Open WebUI</title>\n\n\t\t" + head + "\n\t</head>\n\n\t<body data-sveltekit-preload-data=\"hover\">\n\t\t<div style=\"display: contents\">" + body + "</div>\n\n\t\t<div\n\t\t\tid=\"splash-screen\"\n\t\t\tstyle=\"position: fixed; z-index: 100; top: 0; left: 0; width: 100%; height: 100%\"\n\t\t>\n\t\t\t<style type=\"text/css\" nonce=\"\">\n\t\t\t\thtml {\n\t\t\t\t\toverflow-y: scroll !important;\n\t\t\t\t}\n\t\t\t</style>\n\n\t\t\t<div\n\t\t\t\tstyle=\"\n\t\t\t\t\tposition: absolute;\n\t\t\t\t\ttop: 33%;\n\t\t\t\t\tleft: 50%;\n\n\t\t\t\t\twidth: 24rem;\n\t\t\t\t\ttransform: translateX(-50%);\n\n\t\t\t\t\tdisplay: flex;\n\t\t\t\t\tflex-direction: column;\n\t\t\t\t\talign-items: center;\n\t\t\t\t\"\n\t\t\t>\n\t\t\t\t<img\n\t\t\t\t\tid=\"logo-her\"\n\t\t\t\t\tstyle=\"width: auto; height: 13rem\"\n\t\t\t\t\tsrc=\"/static/splash.png\"\n\t\t\t\t\tclass=\"animate-pulse-fast\"\n\t\t\t\t/>\n\n\t\t\t\t<div style=\"position: relative; width: 24rem; margin-top: 0.5rem\">\n\t\t\t\t\t<div\n\t\t\t\t\t\tid=\"progress-background\"\n\t\t\t\t\t\tstyle=\"\n\t\t\t\t\t\t\tposition: absolute;\n\t\t\t\t\t\t\twidth: 100%;\n\t\t\t\t\t\t\theight: 0.75rem;\n\n\t\t\t\t\t\t\tborder-radius: 9999px;\n\t\t\t\t\t\t\tbackground-color: #fafafa9a;\n\t\t\t\t\t\t\"\n\t\t\t\t\t></div>\n\n\t\t\t\t\t<div\n\t\t\t\t\t\tid=\"progress-bar\"\n\t\t\t\t\t\tstyle=\"\n\t\t\t\t\t\t\tposition: absolute;\n\t\t\t\t\t\t\twidth: 0%;\n\t\t\t\t\t\t\theight: 0.75rem;\n\t\t\t\t\t\t\tborder-radius: 9999px;\n\t\t\t\t\t\t\tbackground-color: #fff;\n\t\t\t\t\t\t\"\n\t\t\t\t\t\tclass=\"bg-white\"\n\t\t\t\t\t></div>\n\t\t\t\t</div>\n\t\t\t</div>\n\n\t\t\t<!-- <span style=\"position: absolute; bottom: 32px; left: 50%; margin: -36px 0 0 -36px\">\n\t\t\t\tFooter content\n\t\t\t</span> -->\n\t\t</div>\n\t</body>\n</html>\n\n<style type=\"text/css\" nonce=\"\">\n\thtml {\n\t\toverflow-y: hidden !important;\n\t\toverscroll-behavior-y: none;\n\t}\n\n\t#splash-screen {\n\t\tbackground: #fff;\n\t}\n\n\thtml.dark #splash-screen {\n\t\tbackground: #000;\n\t}\n\n\thtml.her #splash-screen {\n\t\tbackground: #983724;\n\t}\n\n\t#logo-her {\n\t\tdisplay: none;\n\t}\n\n\t#progress-background {\n\t\tdisplay: none;\n\t}\n\n\t#progress-bar {\n\t\tdisplay: none;\n\t}\n\n\thtml.her #logo {\n\t\tdisplay: none;\n\t}\n\n\thtml.her #logo-her {\n\t\tdisplay: block;\n\t\tfilter: invert(1);\n\t}\n\n\thtml.her #progress-background {\n\t\tdisplay: block;\n\t}\n\n\thtml.her #progress-bar {\n\t\tdisplay: block;\n\t}\n\n\t@media (max-width: 24rem) {\n\t\thtml.her #progress-background {\n\t\t\tdisplay: none;\n\t\t}\n\n\t\thtml.her #progress-bar {\n\t\t\tdisplay: none;\n\t\t}\n\t}\n\n\t@keyframes pulse {\n\t\t50% {\n\t\t\topacity: 0.65;\n\t\t}\n\t}\n\n\t.animate-pulse-fast {\n\t\tanimation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;\n\t}\n</style>\n",
		error: ({ status, message }) => "<!doctype html>\n<html lang=\"en\">\n\t<head>\n\t\t<meta charset=\"utf-8\" />\n\t\t<title>" + message + "</title>\n\n\t\t<style>\n\t\t\tbody {\n\t\t\t\t--bg: white;\n\t\t\t\t--fg: #222;\n\t\t\t\t--divider: #ccc;\n\t\t\t\tbackground: var(--bg);\n\t\t\t\tcolor: var(--fg);\n\t\t\t\tfont-family:\n\t\t\t\t\tsystem-ui,\n\t\t\t\t\t-apple-system,\n\t\t\t\t\tBlinkMacSystemFont,\n\t\t\t\t\t'Segoe UI',\n\t\t\t\t\tRoboto,\n\t\t\t\t\tOxygen,\n\t\t\t\t\tUbuntu,\n\t\t\t\t\tCantarell,\n\t\t\t\t\t'Open Sans',\n\t\t\t\t\t'Helvetica Neue',\n\t\t\t\t\tsans-serif;\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t\tjustify-content: center;\n\t\t\t\theight: 100vh;\n\t\t\t\tmargin: 0;\n\t\t\t}\n\n\t\t\t.error {\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t\tmax-width: 32rem;\n\t\t\t\tmargin: 0 1rem;\n\t\t\t}\n\n\t\t\t.status {\n\t\t\t\tfont-weight: 200;\n\t\t\t\tfont-size: 3rem;\n\t\t\t\tline-height: 1;\n\t\t\t\tposition: relative;\n\t\t\t\ttop: -0.05rem;\n\t\t\t}\n\n\t\t\t.message {\n\t\t\t\tborder-left: 1px solid var(--divider);\n\t\t\t\tpadding: 0 0 0 1rem;\n\t\t\t\tmargin: 0 0 0 1rem;\n\t\t\t\tmin-height: 2.5rem;\n\t\t\t\tdisplay: flex;\n\t\t\t\talign-items: center;\n\t\t\t}\n\n\t\t\t.message h1 {\n\t\t\t\tfont-weight: 400;\n\t\t\t\tfont-size: 1em;\n\t\t\t\tmargin: 0;\n\t\t\t}\n\n\t\t\t@media (prefers-color-scheme: dark) {\n\t\t\t\tbody {\n\t\t\t\t\t--bg: #222;\n\t\t\t\t\t--fg: #ddd;\n\t\t\t\t\t--divider: #666;\n\t\t\t\t}\n\t\t\t}\n\t\t</style>\n\t</head>\n\t<body>\n\t\t<div class=\"error\">\n\t\t\t<span class=\"status\">" + status + "</span>\n\t\t\t<div class=\"message\">\n\t\t\t\t<h1>" + message + "</h1>\n\t\t\t</div>\n\t\t</div>\n\t</body>\n</html>\n"
	},
	version_hash: "yhfgk9"
};

export async function get_hooks() {
	let handle;
	let handleFetch;
	let handleError;
	let handleValidationError;
	let init;
	

	let reroute;
	let transport;
	

	return {
		handle,
		handleFetch,
		handleError,
		handleValidationError,
		init,
		reroute,
		transport
	};
}

export { set_assets, set_building, set_manifest, set_prerendering, set_private_env, set_public_env, set_read_implementation };
