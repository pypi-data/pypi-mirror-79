(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2d2371be"],{fa5b:function(e,n,t){"use strict";t.r(n);var r,i,o,a,u,s,c,d,f,l,g,h,p,m,v,b,y,_,k,w=12e4,x=function(){function e(e){var n=this;this._defaults=e,this._worker=null,this._idleCheckInterval=setInterval(function(){return n._checkIfIdle()},3e4),this._lastUsedTime=0,this._configChangeListener=this._defaults.onDidChange(function(){return n._stopWorker()})}return e.prototype._stopWorker=function(){this._worker&&(this._worker.dispose(),this._worker=null),this._client=null},e.prototype.dispose=function(){clearInterval(this._idleCheckInterval),this._configChangeListener.dispose(),this._stopWorker()},e.prototype._checkIfIdle=function(){if(this._worker){var e=Date.now()-this._lastUsedTime;e>w&&this._stopWorker()}},e.prototype._getClient=function(){return this._lastUsedTime=Date.now(),this._client||(this._worker=monaco.editor.createWebWorker({moduleId:"vs/language/html/htmlWorker",createData:{languageSettings:this._defaults.options,languageId:this._defaults.languageId},label:this._defaults.languageId}),this._client=this._worker.getProxy()),this._client},e.prototype.getLanguageServiceWorker=function(){for(var e,n=this,t=[],r=0;r<arguments.length;r++)t[r]=arguments[r];return this._getClient().then(function(n){e=n}).then(function(e){return n._worker.withSyncedResources(t)}).then(function(n){return e})},e}();(function(e){function n(e,n){return{line:e,character:n}}function t(e){var n=e;return X.objectLiteral(n)&&X.number(n.line)&&X.number(n.character)}e.create=n,e.is=t})(r||(r={})),function(e){function n(e,n,t,i){if(X.number(e)&&X.number(n)&&X.number(t)&&X.number(i))return{start:r.create(e,n),end:r.create(t,i)};if(r.is(e)&&r.is(n))return{start:e,end:n};throw new Error("Range#create called with invalid arguments["+e+", "+n+", "+t+", "+i+"]")}function t(e){var n=e;return X.objectLiteral(n)&&r.is(n.start)&&r.is(n.end)}e.create=n,e.is=t}(i||(i={})),function(e){function n(e,n){return{uri:e,range:n}}function t(e){var n=e;return X.defined(n)&&i.is(n.range)&&(X.string(n.uri)||X.undefined(n.uri))}e.create=n,e.is=t}(o||(o={})),function(e){function n(e,n,t,r){return{targetUri:e,targetRange:n,targetSelectionRange:t,originSelectionRange:r}}function t(e){var n=e;return X.defined(n)&&i.is(n.targetRange)&&X.string(n.targetUri)&&(i.is(n.targetSelectionRange)||X.undefined(n.targetSelectionRange))&&(i.is(n.originSelectionRange)||X.undefined(n.originSelectionRange))}e.create=n,e.is=t}(a||(a={})),function(e){function n(e,n,t,r){return{red:e,green:n,blue:t,alpha:r}}function t(e){var n=e;return X.number(n.red)&&X.number(n.green)&&X.number(n.blue)&&X.number(n.alpha)}e.create=n,e.is=t}(u||(u={})),function(e){function n(e,n){return{range:e,color:n}}function t(e){var n=e;return i.is(n.range)&&u.is(n.color)}e.create=n,e.is=t}(s||(s={})),function(e){function n(e,n,t){return{label:e,textEdit:n,additionalTextEdits:t}}function t(e){var n=e;return X.string(n.label)&&(X.undefined(n.textEdit)||m.is(n))&&(X.undefined(n.additionalTextEdits)||X.typedArray(n.additionalTextEdits,m.is))}e.create=n,e.is=t}(c||(c={})),function(e){e["Comment"]="comment",e["Imports"]="imports",e["Region"]="region"}(d||(d={})),function(e){function n(e,n,t,r,i){var o={startLine:e,endLine:n};return X.defined(t)&&(o.startCharacter=t),X.defined(r)&&(o.endCharacter=r),X.defined(i)&&(o.kind=i),o}function t(e){var n=e;return X.number(n.startLine)&&X.number(n.startLine)&&(X.undefined(n.startCharacter)||X.number(n.startCharacter))&&(X.undefined(n.endCharacter)||X.number(n.endCharacter))&&(X.undefined(n.kind)||X.string(n.kind))}e.create=n,e.is=t}(f||(f={})),function(e){function n(e,n){return{location:e,message:n}}function t(e){var n=e;return X.defined(n)&&o.is(n.location)&&X.string(n.message)}e.create=n,e.is=t}(l||(l={})),function(e){e.Error=1,e.Warning=2,e.Information=3,e.Hint=4}(g||(g={})),function(e){function n(e,n,t,r,i,o){var a={range:e,message:n};return X.defined(t)&&(a.severity=t),X.defined(r)&&(a.code=r),X.defined(i)&&(a.source=i),X.defined(o)&&(a.relatedInformation=o),a}function t(e){var n=e;return X.defined(n)&&i.is(n.range)&&X.string(n.message)&&(X.number(n.severity)||X.undefined(n.severity))&&(X.number(n.code)||X.string(n.code)||X.undefined(n.code))&&(X.string(n.source)||X.undefined(n.source))&&(X.undefined(n.relatedInformation)||X.typedArray(n.relatedInformation,l.is))}e.create=n,e.is=t}(h||(h={})),function(e){function n(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={title:e,command:n};return X.defined(t)&&t.length>0&&(i.arguments=t),i}function t(e){var n=e;return X.defined(n)&&X.string(n.title)&&X.string(n.command)}e.create=n,e.is=t}(p||(p={})),function(e){function n(e,n){return{range:e,newText:n}}function t(e,n){return{range:{start:e,end:e},newText:n}}function r(e){return{range:e,newText:""}}function o(e){var n=e;return X.objectLiteral(n)&&X.string(n.newText)&&i.is(n.range)}e.replace=n,e.insert=t,e.del=r,e.is=o}(m||(m={})),function(e){function n(e,n){return{textDocument:e,edits:n}}function t(e){var n=e;return X.defined(n)&&E.is(n.textDocument)&&Array.isArray(n.edits)}e.create=n,e.is=t}(v||(v={})),function(e){function n(e,n){var t={kind:"create",uri:e};return void 0===n||void 0===n.overwrite&&void 0===n.ignoreIfExists||(t.options=n),t}function t(e){var n=e;return n&&"create"===n.kind&&X.string(n.uri)&&(void 0===n.options||(void 0===n.options.overwrite||X.boolean(n.options.overwrite))&&(void 0===n.options.ignoreIfExists||X.boolean(n.options.ignoreIfExists)))}e.create=n,e.is=t}(b||(b={})),function(e){function n(e,n,t){var r={kind:"rename",oldUri:e,newUri:n};return void 0===t||void 0===t.overwrite&&void 0===t.ignoreIfExists||(r.options=t),r}function t(e){var n=e;return n&&"rename"===n.kind&&X.string(n.oldUri)&&X.string(n.newUri)&&(void 0===n.options||(void 0===n.options.overwrite||X.boolean(n.options.overwrite))&&(void 0===n.options.ignoreIfExists||X.boolean(n.options.ignoreIfExists)))}e.create=n,e.is=t}(y||(y={})),function(e){function n(e,n){var t={kind:"delete",uri:e};return void 0===n||void 0===n.recursive&&void 0===n.ignoreIfNotExists||(t.options=n),t}function t(e){var n=e;return n&&"delete"===n.kind&&X.string(n.uri)&&(void 0===n.options||(void 0===n.options.recursive||X.boolean(n.options.recursive))&&(void 0===n.options.ignoreIfNotExists||X.boolean(n.options.ignoreIfNotExists)))}e.create=n,e.is=t}(_||(_={})),function(e){function n(e){var n=e;return n&&(void 0!==n.changes||void 0!==n.documentChanges)&&(void 0===n.documentChanges||n.documentChanges.every(function(e){return X.string(e.kind)?b.is(e)||y.is(e)||_.is(e):v.is(e)}))}e.is=n}(k||(k={}));var C,E,I,S,T,M,R,F,P,A,D,L,O,j,W,N,U,V=function(){function e(e){this.edits=e}return e.prototype.insert=function(e,n){this.edits.push(m.insert(e,n))},e.prototype.replace=function(e,n){this.edits.push(m.replace(e,n))},e.prototype.delete=function(e){this.edits.push(m.del(e))},e.prototype.add=function(e){this.edits.push(e)},e.prototype.all=function(){return this.edits},e.prototype.clear=function(){this.edits.splice(0,this.edits.length)},e}();(function(){function e(e){var n=this;this._textEditChanges=Object.create(null),e&&(this._workspaceEdit=e,e.documentChanges?e.documentChanges.forEach(function(e){if(v.is(e)){var t=new V(e.edits);n._textEditChanges[e.textDocument.uri]=t}}):e.changes&&Object.keys(e.changes).forEach(function(t){var r=new V(e.changes[t]);n._textEditChanges[t]=r}))}Object.defineProperty(e.prototype,"edit",{get:function(){return this._workspaceEdit},enumerable:!0,configurable:!0}),e.prototype.getTextEditChange=function(e){if(E.is(e)){if(this._workspaceEdit||(this._workspaceEdit={documentChanges:[]}),!this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for document changes.");var n=e,t=this._textEditChanges[n.uri];if(!t){var r=[],i={textDocument:n,edits:r};this._workspaceEdit.documentChanges.push(i),t=new V(r),this._textEditChanges[n.uri]=t}return t}if(this._workspaceEdit||(this._workspaceEdit={changes:Object.create(null)}),!this._workspaceEdit.changes)throw new Error("Workspace edit is not configured for normal text edit changes.");t=this._textEditChanges[e];if(!t){r=[];this._workspaceEdit.changes[e]=r,t=new V(r),this._textEditChanges[e]=t}return t},e.prototype.createFile=function(e,n){this.checkDocumentChanges(),this._workspaceEdit.documentChanges.push(b.create(e,n))},e.prototype.renameFile=function(e,n,t){this.checkDocumentChanges(),this._workspaceEdit.documentChanges.push(y.create(e,n,t))},e.prototype.deleteFile=function(e,n){this.checkDocumentChanges(),this._workspaceEdit.documentChanges.push(_.create(e,n))},e.prototype.checkDocumentChanges=function(){if(!this._workspaceEdit||!this._workspaceEdit.documentChanges)throw new Error("Workspace edit is not configured for document changes.")}})();(function(e){function n(e){return{uri:e}}function t(e){var n=e;return X.defined(n)&&X.string(n.uri)}e.create=n,e.is=t})(C||(C={})),function(e){function n(e,n){return{uri:e,version:n}}function t(e){var n=e;return X.defined(n)&&X.string(n.uri)&&(null===n.version||X.number(n.version))}e.create=n,e.is=t}(E||(E={})),function(e){function n(e,n,t,r){return{uri:e,languageId:n,version:t,text:r}}function t(e){var n=e;return X.defined(n)&&X.string(n.uri)&&X.string(n.languageId)&&X.number(n.version)&&X.string(n.text)}e.create=n,e.is=t}(I||(I={})),function(e){e.PlainText="plaintext",e.Markdown="markdown"}(S||(S={})),function(e){function n(n){var t=n;return t===e.PlainText||t===e.Markdown}e.is=n}(S||(S={})),function(e){function n(e){var n=e;return X.objectLiteral(e)&&S.is(n.kind)&&X.string(n.value)}e.is=n}(T||(T={})),function(e){e.Text=1,e.Method=2,e.Function=3,e.Constructor=4,e.Field=5,e.Variable=6,e.Class=7,e.Interface=8,e.Module=9,e.Property=10,e.Unit=11,e.Value=12,e.Enum=13,e.Keyword=14,e.Snippet=15,e.Color=16,e.File=17,e.Reference=18,e.Folder=19,e.EnumMember=20,e.Constant=21,e.Struct=22,e.Event=23,e.Operator=24,e.TypeParameter=25}(M||(M={})),function(e){e.PlainText=1,e.Snippet=2}(R||(R={})),function(e){function n(e){return{label:e}}e.create=n}(F||(F={})),function(e){function n(e,n){return{items:e||[],isIncomplete:!!n}}e.create=n}(P||(P={})),function(e){function n(e){return e.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}function t(e){var n=e;return X.string(n)||X.objectLiteral(n)&&X.string(n.language)&&X.string(n.value)}e.fromPlainText=n,e.is=t}(A||(A={})),function(e){function n(e){var n=e;return!!n&&X.objectLiteral(n)&&(T.is(n.contents)||A.is(n.contents)||X.typedArray(n.contents,A.is))&&(void 0===e.range||i.is(e.range))}e.is=n}(D||(D={})),function(e){function n(e,n){return n?{label:e,documentation:n}:{label:e}}e.create=n}(L||(L={})),function(e){function n(e,n){for(var t=[],r=2;r<arguments.length;r++)t[r-2]=arguments[r];var i={label:e};return X.defined(n)&&(i.documentation=n),X.defined(t)?i.parameters=t:i.parameters=[],i}e.create=n}(O||(O={})),function(e){e.Text=1,e.Read=2,e.Write=3}(j||(j={})),function(e){function n(e,n){var t={range:e};return X.number(n)&&(t.kind=n),t}e.create=n}(W||(W={})),function(e){e.File=1,e.Module=2,e.Namespace=3,e.Package=4,e.Class=5,e.Method=6,e.Property=7,e.Field=8,e.Constructor=9,e.Enum=10,e.Interface=11,e.Function=12,e.Variable=13,e.Constant=14,e.String=15,e.Number=16,e.Boolean=17,e.Array=18,e.Object=19,e.Key=20,e.Null=21,e.EnumMember=22,e.Struct=23,e.Event=24,e.Operator=25,e.TypeParameter=26}(N||(N={})),function(e){function n(e,n,t,r,i){var o={name:e,kind:n,location:{uri:r,range:t}};return i&&(o.containerName=i),o}e.create=n}(U||(U={}));var H,K,z,B,J,$=function(){function e(){}return e}();(function(e){function n(e,n,t,r,i,o){var a={name:e,detail:n,kind:t,range:r,selectionRange:i};return void 0!==o&&(a.children=o),a}function t(e){var n=e;return n&&X.string(n.name)&&X.number(n.kind)&&i.is(n.range)&&i.is(n.selectionRange)&&(void 0===n.detail||X.string(n.detail))&&(void 0===n.deprecated||X.boolean(n.deprecated))&&(void 0===n.children||Array.isArray(n.children))}e.create=n,e.is=t})($||($={})),function(e){e.QuickFix="quickfix",e.Refactor="refactor",e.RefactorExtract="refactor.extract",e.RefactorInline="refactor.inline",e.RefactorRewrite="refactor.rewrite",e.Source="source",e.SourceOrganizeImports="source.organizeImports"}(H||(H={})),function(e){function n(e,n){var t={diagnostics:e};return void 0!==n&&null!==n&&(t.only=n),t}function t(e){var n=e;return X.defined(n)&&X.typedArray(n.diagnostics,h.is)&&(void 0===n.only||X.typedArray(n.only,X.string))}e.create=n,e.is=t}(K||(K={})),function(e){function n(e,n,t){var r={title:e};return p.is(n)?r.command=n:r.edit=n,void 0!==t&&(r.kind=t),r}function t(e){var n=e;return n&&X.string(n.title)&&(void 0===n.diagnostics||X.typedArray(n.diagnostics,h.is))&&(void 0===n.kind||X.string(n.kind))&&(void 0!==n.edit||void 0!==n.command)&&(void 0===n.command||p.is(n.command))&&(void 0===n.edit||k.is(n.edit))}e.create=n,e.is=t}(z||(z={})),function(e){function n(e,n){var t={range:e};return X.defined(n)&&(t.data=n),t}function t(e){var n=e;return X.defined(n)&&i.is(n.range)&&(X.undefined(n.command)||p.is(n.command))}e.create=n,e.is=t}(B||(B={})),function(e){function n(e,n){return{tabSize:e,insertSpaces:n}}function t(e){var n=e;return X.defined(n)&&X.number(n.tabSize)&&X.boolean(n.insertSpaces)}e.create=n,e.is=t}(J||(J={}));var q=function(){function e(){}return e}();(function(e){function n(e,n,t){return{range:e,target:n,data:t}}function t(e){var n=e;return X.defined(n)&&i.is(n.range)&&(X.undefined(n.target)||X.string(n.target))}e.create=n,e.is=t})(q||(q={}));var Q,G;(function(e){function n(e,n,t,r){return new Y(e,n,t,r)}function t(e){var n=e;return!!(X.defined(n)&&X.string(n.uri)&&(X.undefined(n.languageId)||X.string(n.languageId))&&X.number(n.lineCount)&&X.func(n.getText)&&X.func(n.positionAt)&&X.func(n.offsetAt))}function r(e,n){for(var t=e.getText(),r=i(n,function(e,n){var t=e.range.start.line-n.range.start.line;return 0===t?e.range.start.character-n.range.start.character:t}),o=t.length,a=r.length-1;a>=0;a--){var u=r[a],s=e.offsetAt(u.range.start),c=e.offsetAt(u.range.end);if(!(c<=o))throw new Error("Overlapping edit");t=t.substring(0,s)+u.newText+t.substring(c,t.length),o=s}return t}function i(e,n){if(e.length<=1)return e;var t=e.length/2|0,r=e.slice(0,t),o=e.slice(t);i(r,n),i(o,n);var a=0,u=0,s=0;while(a<r.length&&u<o.length){var c=n(r[a],o[u]);e[s++]=c<=0?r[a++]:o[u++]}while(a<r.length)e[s++]=r[a++];while(u<o.length)e[s++]=o[u++];return e}e.create=n,e.is=t,e.applyEdits=r})(Q||(Q={})),function(e){e.Manual=1,e.AfterDelay=2,e.FocusOut=3}(G||(G={}));var X,Y=function(){function e(e,n,t,r){this._uri=e,this._languageId=n,this._version=t,this._content=r,this._lineOffsets=null}return Object.defineProperty(e.prototype,"uri",{get:function(){return this._uri},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"languageId",{get:function(){return this._languageId},enumerable:!0,configurable:!0}),Object.defineProperty(e.prototype,"version",{get:function(){return this._version},enumerable:!0,configurable:!0}),e.prototype.getText=function(e){if(e){var n=this.offsetAt(e.start),t=this.offsetAt(e.end);return this._content.substring(n,t)}return this._content},e.prototype.update=function(e,n){this._content=e.text,this._version=n,this._lineOffsets=null},e.prototype.getLineOffsets=function(){if(null===this._lineOffsets){for(var e=[],n=this._content,t=!0,r=0;r<n.length;r++){t&&(e.push(r),t=!1);var i=n.charAt(r);t="\r"===i||"\n"===i,"\r"===i&&r+1<n.length&&"\n"===n.charAt(r+1)&&r++}t&&n.length>0&&e.push(n.length),this._lineOffsets=e}return this._lineOffsets},e.prototype.positionAt=function(e){e=Math.max(Math.min(e,this._content.length),0);var n=this.getLineOffsets(),t=0,i=n.length;if(0===i)return r.create(0,e);while(t<i){var o=Math.floor((t+i)/2);n[o]>e?i=o:t=o+1}var a=t-1;return r.create(a,e-n[a])},e.prototype.offsetAt=function(e){var n=this.getLineOffsets();if(e.line>=n.length)return this._content.length;if(e.line<0)return 0;var t=n[e.line],r=e.line+1<n.length?n[e.line+1]:this._content.length;return Math.max(Math.min(t+e.character,r),t)},Object.defineProperty(e.prototype,"lineCount",{get:function(){return this.getLineOffsets().length},enumerable:!0,configurable:!0}),e}();(function(e){var n=Object.prototype.toString;function t(e){return"undefined"!==typeof e}function r(e){return"undefined"===typeof e}function i(e){return!0===e||!1===e}function o(e){return"[object String]"===n.call(e)}function a(e){return"[object Number]"===n.call(e)}function u(e){return"[object Function]"===n.call(e)}function s(e){return null!==e&&"object"===typeof e}function c(e,n){return Array.isArray(e)&&e.every(n)}e.defined=t,e.undefined=r,e.boolean=i,e.string=o,e.number=a,e.func=u,e.objectLiteral=s,e.typedArray=c})(X||(X={}));var Z=monaco.Range,ee=function(){function e(e,n,t){var r=this;this._languageId=e,this._worker=n,this._disposables=[],this._listener=Object.create(null);var i=function(e){var n,t=e.getModeId();t===r._languageId&&(r._listener[e.uri.toString()]=e.onDidChangeContent(function(){clearTimeout(n),n=setTimeout(function(){return r._doValidate(e.uri,t)},500)}),r._doValidate(e.uri,t))},o=function(e){monaco.editor.setModelMarkers(e,r._languageId,[]);var n=e.uri.toString(),t=r._listener[n];t&&(t.dispose(),delete r._listener[n])};this._disposables.push(monaco.editor.onDidCreateModel(i)),this._disposables.push(monaco.editor.onWillDisposeModel(function(e){o(e)})),this._disposables.push(monaco.editor.onDidChangeModelLanguage(function(e){o(e.model),i(e.model)})),this._disposables.push(t.onDidChange(function(e){monaco.editor.getModels().forEach(function(e){e.getModeId()===r._languageId&&(o(e),i(e))})})),this._disposables.push({dispose:function(){for(var e in r._listener)r._listener[e].dispose()}}),monaco.editor.getModels().forEach(i)}return e.prototype.dispose=function(){this._disposables.forEach(function(e){return e&&e.dispose()}),this._disposables=[]},e.prototype._doValidate=function(e,n){this._worker(e).then(function(t){return t.doValidation(e.toString()).then(function(t){var r=t.map(function(n){return te(e,n)});monaco.editor.setModelMarkers(monaco.editor.getModel(e),n,r)})}).then(void 0,function(e){console.error(e)})},e}();function ne(e){switch(e){case g.Error:return monaco.MarkerSeverity.Error;case g.Warning:return monaco.MarkerSeverity.Warning;case g.Information:return monaco.MarkerSeverity.Info;case g.Hint:return monaco.MarkerSeverity.Hint;default:return monaco.MarkerSeverity.Info}}function te(e,n){var t="number"===typeof n.code?String(n.code):n.code;return{severity:ne(n.severity),startLineNumber:n.range.start.line+1,startColumn:n.range.start.character+1,endLineNumber:n.range.end.line+1,endColumn:n.range.end.character+1,message:n.message,code:t,source:n.source}}function re(e){if(e)return{character:e.column-1,line:e.lineNumber-1}}function ie(e){if(e)return{start:re(e.getStartPosition()),end:re(e.getEndPosition())}}function oe(e){if(e)return new Z(e.start.line+1,e.start.character+1,e.end.line+1,e.end.character+1)}function ae(e){var n=monaco.languages.CompletionItemKind;switch(e){case M.Text:return n.Text;case M.Method:return n.Method;case M.Function:return n.Function;case M.Constructor:return n.Constructor;case M.Field:return n.Field;case M.Variable:return n.Variable;case M.Class:return n.Class;case M.Interface:return n.Interface;case M.Module:return n.Module;case M.Property:return n.Property;case M.Unit:return n.Unit;case M.Value:return n.Value;case M.Enum:return n.Enum;case M.Keyword:return n.Keyword;case M.Snippet:return n.Snippet;case M.Color:return n.Color;case M.File:return n.File;case M.Reference:return n.Reference}return n.Property}function ue(e){if(e)return{range:oe(e.range),text:e.newText}}var se=function(){function e(e){this._worker=e}return Object.defineProperty(e.prototype,"triggerCharacters",{get:function(){return[".",":","<",'"',"=","/"]},enumerable:!0,configurable:!0}),e.prototype.provideCompletionItems=function(e,n,t,r){var i=e.uri;return this._worker(i).then(function(e){return e.doComplete(i.toString(),re(n))}).then(function(t){if(t){var r=e.getWordUntilPosition(n),i=new Z(n.lineNumber,r.startColumn,n.lineNumber,r.endColumn),o=t.items.map(function(e){var n={label:e.label,insertText:e.insertText||e.label,sortText:e.sortText,filterText:e.filterText,documentation:e.documentation,detail:e.detail,range:i,kind:ae(e.kind)};return e.textEdit&&(n.range=oe(e.textEdit.range),n.insertText=e.textEdit.newText),e.additionalTextEdits&&(n.additionalTextEdits=e.additionalTextEdits.map(ue)),e.insertTextFormat===R.Snippet&&(n.insertTextRules=monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet),n});return{isIncomplete:t.isIncomplete,suggestions:o}}})},e}();function ce(e){return e&&"object"===typeof e&&"string"===typeof e.kind}function de(e){return"string"===typeof e?{value:e}:ce(e)?"plaintext"===e.kind?{value:e.value.replace(/[\\`*_{}[\]()#+\-.!]/g,"\\$&")}:{value:e.value}:{value:"```"+e.language+"\n"+e.value+"\n```\n"}}function fe(e){if(e)return Array.isArray(e)?e.map(de):[de(e)]}var le=function(){function e(e){this._worker=e}return e.prototype.provideHover=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.doHover(r.toString(),re(n))}).then(function(e){if(e)return{range:oe(e.range),contents:fe(e.contents)}})},e}();function ge(e){var n=monaco.languages.DocumentHighlightKind;switch(e){case j.Read:return n.Read;case j.Write:return n.Write;case j.Text:return n.Text}return n.Text}var he=function(){function e(e){this._worker=e}return e.prototype.provideDocumentHighlights=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.findDocumentHighlights(r.toString(),re(n))}).then(function(e){if(e)return e.map(function(e){return{range:oe(e.range),kind:ge(e.kind)}})})},e}();function pe(e){var n=monaco.languages.SymbolKind;switch(e){case N.File:return n.Array;case N.Module:return n.Module;case N.Namespace:return n.Namespace;case N.Package:return n.Package;case N.Class:return n.Class;case N.Method:return n.Method;case N.Property:return n.Property;case N.Field:return n.Field;case N.Constructor:return n.Constructor;case N.Enum:return n.Enum;case N.Interface:return n.Interface;case N.Function:return n.Function;case N.Variable:return n.Variable;case N.Constant:return n.Constant;case N.String:return n.String;case N.Number:return n.Number;case N.Boolean:return n.Boolean;case N.Array:return n.Array}return n.Function}var me=function(){function e(e){this._worker=e}return e.prototype.provideDocumentSymbols=function(e,n){var t=e.uri;return this._worker(t).then(function(e){return e.findDocumentSymbols(t.toString())}).then(function(e){if(e)return e.map(function(e){return{name:e.name,detail:"",containerName:e.containerName,kind:pe(e.kind),range:oe(e.location.range),selectionRange:oe(e.location.range)}})})},e}(),ve=function(){function e(e){this._worker=e}return e.prototype.provideLinks=function(e,n){var t=e.uri;return this._worker(t).then(function(e){return e.findDocumentLinks(t.toString())}).then(function(e){if(e)return{links:e.map(function(e){return{range:oe(e.range),url:e.target}})}})},e}();function be(e){return{tabSize:e.tabSize,insertSpaces:e.insertSpaces}}var ye=function(){function e(e){this._worker=e}return e.prototype.provideDocumentFormattingEdits=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.format(r.toString(),null,be(n)).then(function(e){if(e&&0!==e.length)return e.map(ue)})})},e}(),_e=function(){function e(e){this._worker=e}return e.prototype.provideDocumentRangeFormattingEdits=function(e,n,t,r){var i=e.uri;return this._worker(i).then(function(e){return e.format(i.toString(),ie(n),be(t)).then(function(e){if(e&&0!==e.length)return e.map(ue)})})},e}(),ke=function(){function e(e){this._worker=e}return e.prototype.provideFoldingRanges=function(e,n,t){var r=e.uri;return this._worker(r).then(function(e){return e.provideFoldingRanges(r.toString(),n)}).then(function(e){if(e)return e.map(function(e){var n={start:e.startLine+1,end:e.endLine+1};return"undefined"!==typeof e.kind&&(n.kind=we(e.kind)),n})})},e}();function we(e){switch(e){case d.Comment:return monaco.languages.FoldingRangeKind.Comment;case d.Imports:return monaco.languages.FoldingRangeKind.Imports;case d.Region:return monaco.languages.FoldingRangeKind.Region}}function xe(e){var n=new x(e),t=function(){for(var e=[],t=0;t<arguments.length;t++)e[t]=arguments[t];return n.getLanguageServiceWorker.apply(n,e)},r=e.languageId;monaco.languages.registerCompletionItemProvider(r,new se(t)),monaco.languages.registerHoverProvider(r,new le(t)),monaco.languages.registerDocumentHighlightProvider(r,new he(t)),monaco.languages.registerLinkProvider(r,new ve(t)),monaco.languages.registerFoldingRangeProvider(r,new ke(t)),monaco.languages.registerDocumentSymbolProvider(r,new me(t)),"html"===r&&(monaco.languages.registerDocumentFormattingEditProvider(r,new ye(t)),monaco.languages.registerDocumentRangeFormattingEditProvider(r,new _e(t)),new ee(r,t,e))}t.d(n,"setupMode",function(){return xe})}}]);