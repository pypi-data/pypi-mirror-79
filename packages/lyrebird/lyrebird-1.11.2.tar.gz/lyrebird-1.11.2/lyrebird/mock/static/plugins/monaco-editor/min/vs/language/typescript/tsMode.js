/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * monaco-typescript version: 3.1.0(64641eebb2d0dca62499cc1b822970ea72efbfce)
 * Released under the MIT license
 * https://github.com/Microsoft/monaco-typescript/blob/master/LICENSE.md
 *-----------------------------------------------------------------------------*/
define("vs/language/typescript/tokenization",["require","exports","./lib/typescriptServices"],function(e,t,f){"use strict";var h,n;Object.defineProperty(t,"__esModule",{value:!0}),(n=h=t.Language||(t.Language={}))[n.TypeScript=0]="TypeScript",n[n.EcmaScript5=1]="EcmaScript5",t.createTokenizationSupport=function(e){var n=f.createClassifier(),r=e===h.TypeScript?i:s,o=e===h.TypeScript?a:c;return{getInitialState:function(){return new v(e,f.EndOfLineState.None,!1)},tokenize:function(e,t){return function(e,t,n,r,o){var i={tokens:[],endState:new v(r.language,f.EndOfLineState.None,!1)};function a(e,t){0!==i.tokens.length&&i.tokens[i.tokens.length-1].scopes===t||i.tokens.push({startIndex:e,scopes:t})}var s=r.language===h.TypeScript;if(!s&&function(e,t,n){if(0===t.indexOf("#!"))return n(e,"comment.shebang"),!0}(0,o,a))return i;var c=n.getClassificationsForLine(o,r.eolState,!0),u=0;i.endState.eolState=c.finalLexState,i.endState.inJsDocComment=c.finalLexState===f.EndOfLineState.InMultiLineCommentTrivia&&(r.inJsDocComment||/\/\*\*.*$/.test(o));for(var l=0,p=c.entries;l<p.length;l++){var d,g=p[l];if(g.classification===f.TokenClass.Punctuation){var m=o.charCodeAt(u);d=e[m]||t[g.classification],a(u,d)}else g.classification===f.TokenClass.Comment?i.endState.inJsDocComment||/\/\*\*.*\*\//.test(o.substr(u,g.length))?a(u,s?"comment.doc.ts":"comment.doc.js"):a(u,s?"comment.ts":"comment.js"):a(u,t[g.classification]||"");u+=g.length}return i}(r,o,n,t,e)}}};var v=function(){function t(e,t,n){this.language=e,this.eolState=t,this.inJsDocComment=n}return t.prototype.clone=function(){return new t(this.language,this.eolState,this.inJsDocComment)},t.prototype.equals=function(e){return e===this||!!(e&&e instanceof t)&&(this.eolState===e.eolState&&this.inJsDocComment===e.inJsDocComment)},t}();var i=Object.create(null);i["(".charCodeAt(0)]="delimiter.parenthesis.ts",i[")".charCodeAt(0)]="delimiter.parenthesis.ts",i["{".charCodeAt(0)]="delimiter.bracket.ts",i["}".charCodeAt(0)]="delimiter.bracket.ts",i["[".charCodeAt(0)]="delimiter.array.ts",i["]".charCodeAt(0)]="delimiter.array.ts";var a=Object.create(null);a[f.TokenClass.Identifier]="identifier.ts",a[f.TokenClass.Keyword]="keyword.ts",a[f.TokenClass.Operator]="delimiter.ts",a[f.TokenClass.Punctuation]="delimiter.ts",a[f.TokenClass.NumberLiteral]="number.ts",a[f.TokenClass.RegExpLiteral]="regexp.ts",a[f.TokenClass.StringLiteral]="string.ts";var s=Object.create(null);s["(".charCodeAt(0)]="delimiter.parenthesis.js",s[")".charCodeAt(0)]="delimiter.parenthesis.js",s["{".charCodeAt(0)]="delimiter.bracket.js",s["}".charCodeAt(0)]="delimiter.bracket.js",s["[".charCodeAt(0)]="delimiter.array.js",s["]".charCodeAt(0)]="delimiter.array.js";var c=Object.create(null);c[f.TokenClass.Identifier]="identifier.js",c[f.TokenClass.Keyword]="keyword.js",c[f.TokenClass.Operator]="delimiter.js",c[f.TokenClass.Punctuation]="delimiter.js",c[f.TokenClass.NumberLiteral]="number.js",c[f.TokenClass.RegExpLiteral]="regexp.js",c[f.TokenClass.StringLiteral]="string.js"}),define("vs/language/typescript/workerManager",["require","exports"],function(e,t){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var c=monaco.Promise,n=function(){function e(e,t){var n=this;this._modeId=e,this._defaults=t,this._worker=null,this._idleCheckInterval=setInterval(function(){return n._checkIfIdle()},3e4),this._lastUsedTime=0,this._configChangeListener=this._defaults.onDidChange(function(){return n._stopWorker()})}return e.prototype._stopWorker=function(){this._worker&&(this._worker.dispose(),this._worker=null),this._client=null},e.prototype.dispose=function(){clearInterval(this._idleCheckInterval),this._configChangeListener.dispose(),this._stopWorker()},e.prototype._checkIfIdle=function(){if(this._worker){var e=this._defaults.getWorkerMaxIdleTime(),t=Date.now()-this._lastUsedTime;0<e&&e<t&&this._stopWorker()}},e.prototype._getClient=function(){var t=this;if(this._lastUsedTime=Date.now(),!this._client){this._worker=monaco.editor.createWebWorker({moduleId:"vs/language/typescript/tsWorker",label:this._modeId,createData:{compilerOptions:this._defaults.getCompilerOptions(),extraLibs:this._defaults.getExtraLibs()}});var e=this._worker.getProxy();this._defaults.getEagerModelSync()&&(e=e.then(function(e){return t._worker.withSyncedResources(monaco.editor.getModels().filter(function(e){return e.getModeId()===t._modeId}).map(function(e){return e.uri}))})),this._client=e}return this._client},e.prototype.getLanguageServiceWorker=function(){for(var t,e,n,r,o,i=this,a=[],s=0;s<arguments.length;s++)a[s]=arguments[s];return e=this._getClient().then(function(e){t=e}).then(function(e){return i._worker.withSyncedResources(a)}).then(function(e){return t}),o=new c(function(e,t){n=e,r=t},function(){}),e.then(n,r),o},e}();t.WorkerManager=n});var __extends=this&&this.__extends||function(){var r=Object.setPrototypeOf||{__proto__:[]}instanceof Array&&function(e,t){e.__proto__=t}||function(e,t){for(var n in t)t.hasOwnProperty(n)&&(e[n]=t[n])};return function(e,t){function n(){this.constructor=e}r(e,t),e.prototype=null===t?Object.create(t):(n.prototype=t.prototype,new n)}}();define("vs/language/typescript/languageFeatures",["require","exports","./lib/typescriptServices"],function(e,t,c){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var s=monaco.Uri,u=monaco.Promise,n=function(){function e(e){this._worker=e}return e.prototype._positionToOffset=function(e,t){return monaco.editor.getModel(e).getOffsetAt(t)},e.prototype._offsetToPosition=function(e,t){return monaco.editor.getModel(e).getPositionAt(t)},e.prototype._textSpanToRange=function(e,t){var n=this._offsetToPosition(e,t.start),r=this._offsetToPosition(e,t.start+t.length);return{startLineNumber:n.lineNumber,startColumn:n.column,endLineNumber:r.lineNumber,endColumn:r.column}},e}(),r=function(n){function e(e,r,t){var o=n.call(this,t)||this;o._defaults=e,o._selector=r,o._disposables=[],o._listener=Object.create(null);var i=function(e){if(e.getModeId()===r){var t,n=e.onDidChangeContent(function(){clearTimeout(t),t=setTimeout(function(){return o._doValidate(e.uri)},500)});o._listener[e.uri.toString()]={dispose:function(){n.dispose(),clearTimeout(t)}},o._doValidate(e.uri)}},a=function(e){monaco.editor.setModelMarkers(e,o._selector,[]);var t=e.uri.toString();o._listener[t]&&(o._listener[t].dispose(),delete o._listener[t])};return o._disposables.push(monaco.editor.onDidCreateModel(i)),o._disposables.push(monaco.editor.onWillDisposeModel(a)),o._disposables.push(monaco.editor.onDidChangeModelLanguage(function(e){a(e.model),i(e.model)})),o._disposables.push({dispose:function(){for(var e=0,t=monaco.editor.getModels();e<t.length;e++){var n=t[e];a(n)}}}),o._disposables.push(o._defaults.onDidChange(function(){for(var e=0,t=monaco.editor.getModels();e<t.length;e++){var n=t[e];a(n),i(n)}})),monaco.editor.getModels().forEach(i),o}return __extends(e,n),e.prototype.dispose=function(){this._disposables.forEach(function(e){return e&&e.dispose()}),this._disposables=[]},e.prototype._doValidate=function(i){var a=this;this._worker(i).then(function(e){if(!monaco.editor.getModel(i))return null;var t=[],n=a._defaults.getDiagnosticsOptions(),r=n.noSyntaxValidation,o=n.noSemanticValidation;return r||t.push(e.getSyntacticDiagnostics(i.toString())),o||t.push(e.getSemanticDiagnostics(i.toString())),u.join(t)}).then(function(e){if(!e||!monaco.editor.getModel(i))return null;var t=e.reduce(function(e,t){return t.concat(e)},[]).map(function(e){return a._convertDiagnostics(i,e)});monaco.editor.setModelMarkers(monaco.editor.getModel(i),a._selector,t)}).done(void 0,function(e){console.error(e)})},e.prototype._convertDiagnostics=function(e,t){var n=this._offsetToPosition(e,t.start),r=n.lineNumber,o=n.column,i=this._offsetToPosition(e,t.start+t.length),a=i.lineNumber,s=i.column;return{severity:monaco.MarkerSeverity.Error,startLineNumber:r,startColumn:o,endLineNumber:a,endColumn:s,message:c.flattenDiagnosticMessageText(t.messageText,"\n")}},e}(t.Adapter=n);t.DiagnostcsAdapter=r;var o=function(e){function a(){return null!==e&&e.apply(this,arguments)||this}return __extends(a,e),Object.defineProperty(a.prototype,"triggerCharacters",{get:function(){return["."]},enumerable:!0,configurable:!0}),a.prototype.provideCompletionItems=function(e,t,n){e.getWordUntilPosition(t);var r=e.uri,o=this._positionToOffset(r,t);return _(n,this._worker(r).then(function(e){return e.getCompletionsAtPosition(r.toString(),o)}).then(function(e){if(e)return e.entries.map(function(e){return{uri:r,position:t,label:e.name,sortText:e.sortText,kind:a.convertKind(e.kind)}})}))},a.prototype.resolveCompletionItem=function(e,t){var n=this,r=e,o=r.uri,i=r.position;return _(t,this._worker(o).then(function(e){return e.getCompletionEntryDetails(o.toString(),n._positionToOffset(o,i),r.label)}).then(function(e){return e?{uri:o,position:i,label:e.name,kind:a.convertKind(e.kind),detail:c.displayPartsToString(e.displayParts),documentation:c.displayPartsToString(e.documentation)}:r}))},a.convertKind=function(e){switch(e){case m.primitiveType:case m.keyword:return monaco.languages.CompletionItemKind.Keyword;case m.variable:case m.localVariable:return monaco.languages.CompletionItemKind.Variable;case m.memberVariable:case m.memberGetAccessor:case m.memberSetAccessor:return monaco.languages.CompletionItemKind.Field;case m.function:case m.memberFunction:case m.constructSignature:case m.callSignature:case m.indexSignature:return monaco.languages.CompletionItemKind.Function;case m.enum:return monaco.languages.CompletionItemKind.Enum;case m.module:return monaco.languages.CompletionItemKind.Module;case m.class:return monaco.languages.CompletionItemKind.Class;case m.interface:return monaco.languages.CompletionItemKind.Interface;case m.warning:return monaco.languages.CompletionItemKind.File}return monaco.languages.CompletionItemKind.Property},a}(n);t.SuggestAdapter=o;var i=function(t){function e(){var e=null!==t&&t.apply(this,arguments)||this;return e.signatureHelpTriggerCharacters=["(",","],e}return __extends(e,t),e.prototype.provideSignatureHelp=function(e,t,n){var r=this,o=e.uri;return _(n,this._worker(o).then(function(e){return e.getSignatureHelpItems(o.toString(),r._positionToOffset(o,t))}).then(function(e){if(e){var t={activeSignature:e.selectedItemIndex,activeParameter:e.argumentIndex,signatures:[]};return e.items.forEach(function(i){var a={label:"",documentation:null,parameters:[]};a.label+=c.displayPartsToString(i.prefixDisplayParts),i.parameters.forEach(function(e,t,n){var r=c.displayPartsToString(e.displayParts),o={label:r,documentation:c.displayPartsToString(e.documentation)};a.label+=r,a.parameters.push(o),t<n.length-1&&(a.label+=c.displayPartsToString(i.separatorDisplayParts))}),a.label+=c.displayPartsToString(i.suffixDisplayParts),t.signatures.push(a)}),t}}))},e}(n);t.SignatureHelpAdapter=i;var a=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t.prototype.provideHover=function(e,t,n){var o=this,i=e.uri;return _(n,this._worker(i).then(function(e){return e.getQuickInfoAtPosition(i.toString(),o._positionToOffset(i,t))}).then(function(e){if(e){var t=c.displayPartsToString(e.documentation),n=e.tags?e.tags.map(function(e){var t="*@"+e.name+"*";return e.text?t+(e.text.match(/\r\n|\n/g)?" \n"+e.text:" - "+e.text):t}).join("  \n\n"):"",r=c.displayPartsToString(e.displayParts);return{range:o._textSpanToRange(i,e.textSpan),contents:[{value:r},{value:t+(n?"\n\n"+n:"")}]}}}))},t}(n);t.QuickInfoAdapter=a;var l=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t.prototype.provideDocumentHighlights=function(e,t,n){var r=this,o=e.uri;return _(n,this._worker(o).then(function(e){return e.getOccurrencesAtPosition(o.toString(),r._positionToOffset(o,t))}).then(function(e){if(e)return e.map(function(e){return{range:r._textSpanToRange(o,e.textSpan),kind:e.isWriteAccess?monaco.languages.DocumentHighlightKind.Write:monaco.languages.DocumentHighlightKind.Text}})}))},t}(n);t.OccurrencesAdapter=l;var p=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t.prototype.provideDefinition=function(e,t,n){var a=this,r=e.uri;return _(n,this._worker(r).then(function(e){return e.getDefinitionAtPosition(r.toString(),a._positionToOffset(r,t))}).then(function(e){if(e){for(var t=[],n=0,r=e;n<r.length;n++){var o=r[n],i=s.parse(o.fileName);monaco.editor.getModel(i)&&t.push({uri:i,range:a._textSpanToRange(i,o.textSpan)})}return t}}))},t}(n);t.DefinitionAdapter=p;var d=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t.prototype.provideReferences=function(e,t,n,r){var a=this,o=e.uri;return _(r,this._worker(o).then(function(e){return e.getReferencesAtPosition(o.toString(),a._positionToOffset(o,t))}).then(function(e){if(e){for(var t=[],n=0,r=e;n<r.length;n++){var o=r[n],i=s.parse(o.fileName);monaco.editor.getModel(i)&&t.push({uri:i,range:a._textSpanToRange(i,o.textSpan)})}return t}}))},t}(n);t.ReferenceAdapter=d;var g=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t.prototype.provideDocumentSymbols=function(e,t){var c=this,u=e.uri;return _(t,this._worker(u).then(function(e){return e.getNavigationBarItems(u.toString())}).then(function(e){if(e){var s=function(e,t,n){var r={name:t.text,kind:f[t.kind]||monaco.languages.SymbolKind.Variable,location:{uri:u,range:c._textSpanToRange(u,t.spans[0])},containerName:n};if(t.childItems&&0<t.childItems.length)for(var o=0,i=t.childItems;o<i.length;o++){var a=i[o];s(e,a,r.name)}e.push(r)},t=[];return e.forEach(function(e){return s(t,e)}),t}}))},t}(n);t.OutlineAdapter=g;var m=function(){function e(){}return e.unknown="",e.keyword="keyword",e.script="script",e.module="module",e.class="class",e.interface="interface",e.type="type",e.enum="enum",e.variable="var",e.localVariable="local var",e.function="function",e.localFunction="local function",e.memberFunction="method",e.memberGetAccessor="getter",e.memberSetAccessor="setter",e.memberVariable="property",e.constructorImplementation="constructor",e.callSignature="call",e.indexSignature="index",e.constructSignature="construct",e.parameter="parameter",e.typeParameter="type parameter",e.primitiveType="primitive type",e.label="label",e.alias="alias",e.const="const",e.let="let",e.warning="warning",e}();t.Kind=m;var f=Object.create(null);f[m.module]=monaco.languages.SymbolKind.Module,f[m.class]=monaco.languages.SymbolKind.Class,f[m.enum]=monaco.languages.SymbolKind.Enum,f[m.interface]=monaco.languages.SymbolKind.Interface,f[m.memberFunction]=monaco.languages.SymbolKind.Method,f[m.memberVariable]=monaco.languages.SymbolKind.Property,f[m.memberGetAccessor]=monaco.languages.SymbolKind.Property,f[m.memberSetAccessor]=monaco.languages.SymbolKind.Property,f[m.variable]=monaco.languages.SymbolKind.Variable,f[m.const]=monaco.languages.SymbolKind.Variable,f[m.localVariable]=monaco.languages.SymbolKind.Variable,f[m.variable]=monaco.languages.SymbolKind.Variable,f[m.function]=monaco.languages.SymbolKind.Function,f[m.localFunction]=monaco.languages.SymbolKind.Function;var h=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t._convertOptions=function(e){return{ConvertTabsToSpaces:e.insertSpaces,TabSize:e.tabSize,IndentSize:e.tabSize,IndentStyle:c.IndentStyle.Smart,NewLineCharacter:"\n",InsertSpaceAfterCommaDelimiter:!0,InsertSpaceAfterSemicolonInForStatements:!0,InsertSpaceBeforeAndAfterBinaryOperators:!0,InsertSpaceAfterKeywordsInControlFlowStatements:!0,InsertSpaceAfterFunctionKeywordForAnonymousFunctions:!0,InsertSpaceAfterOpeningAndBeforeClosingNonemptyParenthesis:!1,InsertSpaceAfterOpeningAndBeforeClosingNonemptyBrackets:!1,InsertSpaceAfterOpeningAndBeforeClosingTemplateStringBraces:!1,PlaceOpenBraceOnNewLineForControlBlocks:!1,PlaceOpenBraceOnNewLineForFunctions:!1}},t.prototype._convertTextChanges=function(e,t){return{text:t.newText,range:this._textSpanToRange(e,t.span)}},t}(n),v=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),t.prototype.provideDocumentRangeFormattingEdits=function(e,t,n,r){var o=this,i=e.uri;return _(r,this._worker(i).then(function(e){return e.getFormattingEditsForRange(i.toString(),o._positionToOffset(i,{lineNumber:t.startLineNumber,column:t.startColumn}),o._positionToOffset(i,{lineNumber:t.endLineNumber,column:t.endColumn}),h._convertOptions(n))}).then(function(e){if(e)return e.map(function(e){return o._convertTextChanges(i,e)})}))},t}(t.FormatHelper=h);t.FormatAdapter=v;var y=function(e){function t(){return null!==e&&e.apply(this,arguments)||this}return __extends(t,e),Object.defineProperty(t.prototype,"autoFormatTriggerCharacters",{get:function(){return[";","}","\n"]},enumerable:!0,configurable:!0}),t.prototype.provideOnTypeFormattingEdits=function(e,t,n,r,o){var i=this,a=e.uri;return _(o,this._worker(a).then(function(e){return e.getFormattingEditsAfterKeystroke(a.toString(),i._positionToOffset(a,t),n,h._convertOptions(r))}).then(function(e){if(e)return e.map(function(e){return i._convertTextChanges(a,e)})}))},t}(h);function _(e,t){return e.onCancellationRequested(function(){return t.cancel()}),t}t.FormatOnTypeAdapter=y}),define("vs/language/typescript/tsMode",["require","exports","./tokenization","./workerManager","./languageFeatures"],function(e,t,i,a,s){"use strict";var n,r;function o(e,t,n){var r=new a.WorkerManager(t,e),o=function(e){for(var t=[],n=1;n<arguments.length;n++)t[n-1]=arguments[n];return r.getLanguageServiceWorker.apply(r,[e].concat(t))};return monaco.languages.registerCompletionItemProvider(t,new s.SuggestAdapter(o)),monaco.languages.registerSignatureHelpProvider(t,new s.SignatureHelpAdapter(o)),monaco.languages.registerHoverProvider(t,new s.QuickInfoAdapter(o)),monaco.languages.registerDocumentHighlightProvider(t,new s.OccurrencesAdapter(o)),monaco.languages.registerDefinitionProvider(t,new s.DefinitionAdapter(o)),monaco.languages.registerReferenceProvider(t,new s.ReferenceAdapter(o)),monaco.languages.registerDocumentSymbolProvider(t,new s.OutlineAdapter(o)),monaco.languages.registerDocumentRangeFormattingEditProvider(t,new s.FormatAdapter(o)),monaco.languages.registerOnTypeFormattingEditProvider(t,new s.FormatOnTypeAdapter(o)),new s.DiagnostcsAdapter(e,t,o),monaco.languages.setLanguageConfiguration(t,c),monaco.languages.setTokensProvider(t,i.createTokenizationSupport(n)),o}Object.defineProperty(t,"__esModule",{value:!0}),t.setupTypeScript=function(e){r=o(e,"typescript",i.Language.TypeScript)},t.setupJavaScript=function(e){n=o(e,"javascript",i.Language.EcmaScript5)},t.getJavaScriptWorker=function(){return new monaco.Promise(function(e,t){if(!n)return t("JavaScript not registered!");e(n)})},t.getTypeScriptWorker=function(){return new monaco.Promise(function(e,t){if(!r)return t("TypeScript not registered!");e(r)})};var c={wordPattern:/(-?\d*\.\d\w*)|([^\`\~\!\@\#\%\^\&\*\(\)\-\=\+\[\{\]\}\\\|\;\:\'\"\,\.\<\>\/\?\s]+)/g,comments:{lineComment:"//",blockComment:["/*","*/"]},brackets:[["{","}"],["[","]"],["(",")"]],onEnterRules:[{beforeText:/^\s*\/\*\*(?!\/)([^\*]|\*(?!\/))*$/,afterText:/^\s*\*\/$/,action:{indentAction:monaco.languages.IndentAction.IndentOutdent,appendText:" * "}},{beforeText:/^\s*\/\*\*(?!\/)([^\*]|\*(?!\/))*$/,action:{indentAction:monaco.languages.IndentAction.None,appendText:" * "}},{beforeText:/^(\t|(\ \ ))*\ \*(\ ([^\*]|\*(?!\/))*)?$/,action:{indentAction:monaco.languages.IndentAction.None,appendText:"* "}},{beforeText:/^(\t|(\ \ ))*\ \*\/\s*$/,action:{indentAction:monaco.languages.IndentAction.None,removeText:1}}],autoClosingPairs:[{open:"{",close:"}"},{open:"[",close:"]"},{open:"(",close:")"},{open:'"',close:'"',notIn:["string"]},{open:"'",close:"'",notIn:["string","comment"]},{open:"`",close:"`",notIn:["string","comment"]},{open:"/**",close:" */",notIn:["string"]}],folding:{markers:{start:new RegExp("^\\s*//\\s*#?region\\b"),end:new RegExp("^\\s*//\\s*#?endregion\\b")}}}});