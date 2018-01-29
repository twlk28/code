/* lexical grammar */
%lex
%%

\s+                   	/* skip whitespace */
"-"?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+-]?\d+)?				return 'Number'
\"(((?=\\)\\(["\\\/bfnrt]|u[0-9a-fA-F]{4}))|[^"\\]+)*\"		return 'String'
"true"					return 'True'
"false"					return 'False'
"null"					return 'Null'
"["					  	return 'BracketL'
"]"					  	return 'BracketR'
"{"					  	return 'BraceL'
"}"					  	return 'BraceR'
","					  	return 'Comma'
":"						return 'Colon'
<<EOF>>               	return 'EOF'

/lex

%start expressions

%% /* language grammar */

expressions: 
	value EOF {
		console.log($1)
    	return $1;
    }
    ;

value:
	number {
		$$ = $1
	}
	| string {
		$$ = $1
	}
	| array {
		$$ = $1
	}
	| dict {
		$$ = $1
	} 
	| True {
		$$ = true
	}
	| False {
		$$ = false
	}
	| Null {
		$$ = null
	}
	;

array:
	BracketL elements BracketR {
		if ($2.length == 0){
			$$ = []
		}
		else {
			$$ = $2
		}
	}
	;

elements:
	value {
		$$ = [$1]
	}
	| elements Comma value {
		$1.push($3)
		$$ = $1
	}
	;

dict:
	BraceL pairs BraceR {
		d = {}
		$2.forEach(function(e){
			d[e[0]] = e[1]
		})
		$$ = d
	}
	;

pairs:
	pair {
		$$ = [$1]
	}
	| pairs Comma pair {
		$1.push($3)
		$$ = $1
	}
	;

pair:
	string Colon value {
		$$ = [$1, $3]
	}	
	;

string:
	String {
		$$ = $1.slice(1, -1)
	}
	;

number:
	Number {
		$$ = parseFloat($1)
	}	
	;
