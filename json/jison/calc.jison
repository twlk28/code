/* lexical grammar */
%lex
%%

\s+                   /* skip whitespace */
[0-9]+("."[0-9]+)?    return 'NUMBER'
"+"					  return 'PLUS'
"-"					  return 'SUB'
"*"					  return 'MULTI'
"/"					  return 'DIV'
"("					  return 'BL'
")"					  return 'BR'
.                     return 'INVALID'
<<EOF>>               return 'EOF'

/lex

%start expressions

%% /* language grammar */

expressions: 
	statement EOF {
		console.log($1);
    	return $1;
    }
    ;

statement:
	term PLUS term {
		$$ = $1 + $3
	}
	| term SUB term {
		$$ = $1 - $3
	}
	| term {
		$$ = $1
	}
	;

term:
	factor MULTI factor {
		$$ = $1 * $3
	}
	| factor DIV factor {
		$$ = $1 / $3
	}
	| factor {
		$$ = $1
	}
	;

factor:
	NUMBER {
		$$ = parseFloat($1)
	}
	| BL statement BR {
		$$ = $2
	}
	;
